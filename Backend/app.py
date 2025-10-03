from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import sqlite3
import pickle
import torch
from transformers import pipeline
import numpy as np
from googletrans import Translator, LANGUAGES

app = FastAPI(title="Green Matchers API")

# Load models
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dims, multilingual-capable
generator = pipeline("text-generation", model="gpt2", device=0 if torch.cuda.is_available() else -1, 
                     max_new_tokens=50, truncation=True)
translator = Translator()

DB_FILE = 'green_jobs.db'

# Supported languages (10 major Indian + English)
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
    lang: str = "en"  # Default to English, user can specify language

class JobInput(BaseModel):
    job_title: str
    job_description: str
    lang: str = "en"  # Default to English

class QueryInput(BaseModel):
    skill_text: str
    lang: str = "en"  # Language for narrative

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills_vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_text TEXT NOT NULL,
                embedding BLOB
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs_vectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                job_description TEXT NOT NULL,
                embedding BLOB
            )
        """)
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")
    finally:
        cursor.close()
        conn.close()

init_db()

def get_db_connection():
    return sqlite3.connect(DB_FILE)

def translate_text(text, target_lang="en", source_lang="auto"):
    try:
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {target_lang}")
        return translator.translate(text, dest=SUPPORTED_LANGUAGES[target_lang], src=source_lang).text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")

@app.post("/add_skill")
def add_skill(skill: SkillInput):
    # Translate skill to English for embedding
    translated_skill = translate_text(skill.skill_text, "en", skill.lang)
    embedding = model.encode([translated_skill])[0]
    emb_bin = pickle.dumps(embedding)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO skills_vectors (skill_text, embedding) VALUES (?, ?)", 
                       (skill.skill_text, emb_bin))
        conn.commit()
        return {"message": "Skill added", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/add_job")
def add_job(job: JobInput):
    # Translate job details to English
    translated_title = translate_text(job.job_title, "en", job.lang)
    translated_desc = translate_text(job.job_description, "en", job.lang)
    text = f"{translated_title}: {translated_desc}"
    embedding = model.encode([text])[0]
    emb_bin = pickle.dumps(embedding)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO jobs_vectors (job_title, job_description, embedding) VALUES (?, ?, ?)", 
                       (job.job_title, job.job_description, emb_bin))
        conn.commit()
        return {"message": "Job added", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/match_jobs")
def match_jobs(query: QueryInput):
    # Translate query to English for matching
    translated_query = translate_text(query.skill_text, "en", query.lang)
    q_embedding = model.encode([translated_query])[0]
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, job_title, job_description, embedding FROM jobs_vectors")
        jobs = cursor.fetchall()
        if not jobs:
            return []
        matches = []
        for job in jobs:
            j_emb = pickle.loads(job[3])
            similarity = float(np.dot(q_embedding, j_emb))
            matches.append({
                "id": job[0],
                "job_title": job[1],
                "description": job[2],
                "similarity": similarity
            })
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        return matches[:5]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/generate_narrative")
def generate_narrative(query: QueryInput):
    # Generate in English, then translate to requested language
    prompt = f"In an inspiring tone, tell a 50-word story of how {query.skill_text} drives green jobs like renewable energy or waste reduction:"
    try:
        narrative_en = generator(prompt, max_length=100, num_return_sequences=1, do_sample=True)[0]['generated_text'].strip()[:150]
        narrative = translate_text(narrative_en, query.lang, "en")
        return {"narrative": narrative}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



