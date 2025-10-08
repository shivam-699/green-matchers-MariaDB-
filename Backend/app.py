from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import mariadb
import torch
from transformers import pipeline
import numpy as np
np.linalg.norm
from deep_translator import GoogleTranslator

import os
from dotenv import load_dotenv

app = FastAPI(title="Green Matchers API")

from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


# Load models
def load_models() -> None:
    global model, generator  #declare as global
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')  # 384 dims, multilingual-capable
    generator = pipeline("text-generation", model="gpt2", device=0 if torch.cuda.is_available() else -1, 
                        max_new_tokens=100, truncation=True)
    
#initialize models
load_models()
def regenerate_embeddings():
    conn = mariadb.connect(
        host="localhost",
        user="root",
        password="Shivam@12345",
        database="green_matchers_db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, job_title, job_description FROM jobs_vectors")
    jobs = cursor.fetchall()
    for job in jobs:
        job_id, title, desc = job
        text = f"{title} {desc}"
        embedding = model.encode(text).astype('float32').tobytes()
        cursor.execute(
            "UPDATE jobs_vectors SET embedding = %s WHERE id = %s",
            (embedding, job_id)
        )
    conn.commit()
    conn.close()



    
# Load environment variables
load_dotenv()
#debug line
print("Current dir:", os.getcwd(), "DB_PASSWORD:", os.getenv("DB_PASSWORD"))  # Debug line
# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,  # Matches your server port
    "user": "root",
    "password": os.getenv("DB_PASSWORD", "Shivam@12345"),  # Matches your working password
    "database": "green_matchers_db"
}

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "english",
    "hi": "hindi",
    "bn": "bengali",
    "mr": "marathi",
    "te": "telugu",
    "ta": "tamil",
    "gu": "gujarati",
    "ur": "urdu",
    "kn": "kannada",
    "or": "odia",
    "ml": "malayalam"
}

class SkillInput(BaseModel):
    skill_text: str
    lang: str = "en"

class JobInput(BaseModel):
    job_title: str
    job_description: str
    lang: str = "en"

class QueryInput(BaseModel):
    skill_text: list[str]
    lang: str = "en"

# Initialize database
def init_db():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills_vectors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                skill_text VARCHAR(255) NOT NULL,
                embedding BLOB
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs_vectors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                job_title VARCHAR(255) NOT NULL,
                job_description TEXT NOT NULL,
                embedding BLOB
            )
        """)
        conn.commit()
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

init_db()

def get_db_connection():
    return mariadb.connect(**DB_CONFIG)

def translate_text(text, target_lang="en", source_lang="auto"):
    try:
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {target_lang}")
        return GoogleTranslator(source=source_lang, target=SUPPORTED_LANGUAGES[target_lang]).translate(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.post("/add_skill")
def add_skill(skill: SkillInput):
    translated_skill = translate_text(skill.skill_text, "en", skill.lang)
    embedding = model.encode([translated_skill])[0].astype(np.float32).tobytes()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO skills_vectors (skill_text, embedding) VALUES (?, ?)", 
                      (skill.skill_text, embedding))
        conn.commit()
        return {"message": "Skill added", "id": cursor.lastrowid}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/add_job")
def add_job(job: JobInput):
    translated_title = translate_text(job.job_title, "en", job.lang)
    translated_desc = translate_text(job.job_description, "en", job.lang)
    text = f"{translated_title}: {translated_desc}"
    embedding = model.encode([text])[0].astype(np.float32).tobytes()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO jobs_vectors (job_title, job_description, embedding) VALUES (?, ?, ?)", 
                      (job.job_title, job.job_description, embedding))
        conn.commit()
        return {"message": "Job added", "id": cursor.lastrowid}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/match_jobs")
async def match_jobs(query: QueryInput):
    translated_skills = [translate_text(skill, "en", query.lang) for skill in query.skill_text]
    q_embedding = model.encode(translated_skills).mean(axis=0).astype(np.float32).tobytes()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, job_title, job_description, embedding FROM jobs_vectors")
        jobs = cursor.fetchall()
        if not jobs:
            # No jobs—suggest default skills with links
            suggestions = [
                {"skill": "Python", "link": "https://www.coursera.org/learn/python"},
                {"skill": "Renewable Energy Basics", "link": "https://www.coursera.org/specializations/renewable-energy"},
                {"skill": "Waste Management", "link": "https://www.linkedin.com/learning/sustainable-waste-management"}
            ]
            return {"matches": [], "suggestions": suggestions}
        matches = []
        for job in jobs:
            j_emb = np.frombuffer(job[3], dtype=np.float32)
#added correction line
            q_emb_array = np.frombuffer(q_embedding, dtype=np.float32)
            q_norm = np.linalg.norm(q_emb_array)
            j_norm = np.linalg.norm(j_emb)
            if q_norm == 0 or j_norm == 0:
                similarity = 0.0  # Avoid division by zero
            else:
                similarity = float(np.dot(q_emb_array, j_emb) / (q_norm * j_norm))
#till here
            matches.append({
                "id": job[0],
                "job_title": job[1],
                "description": job[2],
                "similarity": similarity
            })
        matches.sort(key=lambda x: x["similarity"], reverse=True)

        if matches:
            await manager.broadcast(f"New matches found: {len(matches)} jobs matched with similarity > 0.8")
        
        suggestions = []
        if all(m["similarity"] < 0.8 for m in matches):
            suggestions = [
                {"skill": "API design", "link": "https://www.coursera.org/learn/api-design-apigee-gcp"},
                {"skill": "Renewable Energy Basics", "link": "https://www.coursera.org/specializations/renewable-energy"},
                {"skill": "Waste Management", "link": "https://www.linkedin.com/learning/sustainable-waste-management"}
            ]
        return {"matches": matches[:5], "suggestions": suggestions}
    except mariadb.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/generate_narrative")
def generate_narrative(query: QueryInput):
    skill_text = ", ".join(query.skill_text)
    prompt = f"In an inspiring tone, tell a 50-word story of how {skill_text} drives green jobs like renewable energy or waste reduction:"
    try:
        narrative_en = generator(prompt, max_length=100, num_return_sequences=1, do_sample=True)[0]['generated_text'].strip()[:150]
        narrative = translate_text(narrative_en, query.lang, "en")
        return {"narrative": narrative}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left")


if __name__ == "__main__":
    import uvicorn
    load_models()
    regenerate_embeddings()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



