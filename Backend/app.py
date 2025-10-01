from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import sqlite3
import pickle

app = FastAPI(title="Green Matchers API")

# Load model (CPU-friendly, 384 dims)
model = SentenceTransformer('all-MiniLM-L6-v2')

DB_FILE = 'green_jobs.db'

class SkillInput(BaseModel):
    skill_text: str

class JobInput(BaseModel):
    job_title: str
    job_description: str

def get_db_connection():
    return sqlite3.connect(DB_FILE)

@app.post("/add_skill")
def add_skill(skill: SkillInput):
    embedding = model.encode(skill.skill_text)
    emb_bin = pickle.dumps(embedding)  # Binary for DB
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO skills_vectors (skill_text, embedding) VALUES (?, ?)", (skill.skill_text, emb_bin))
        conn.commit()
        return {"message": "Skill added", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/add_job")
def add_job(job: JobInput):
    text = f"{job.job_title}: {job.job_description}"
    embedding = model.encode(text)
    emb_bin = pickle.dumps(embedding)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO jobs_vectors (job_title, job_description, embedding) VALUES (?, ?, ?)", (job.job_title, job.job_description, emb_bin))
        conn.commit()
        return {"message": "Job added", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":

    import numpy as np  # For dot product (add this to the top imports if not there)

class QueryInput(BaseModel):
    skill_text: str

@app.post("/match_jobs")
def match_jobs(query: QueryInput):
    q_embedding = model.encode(query.skill_text)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, job_title, job_description, embedding FROM jobs_vectors")
        jobs = cursor.fetchall()
        matches = []
        for job in jobs:
            j_emb = pickle.loads(job[3])  # Deserialize binary embedding
            similarity = np.dot(q_embedding, j_emb)  # Dot product score
            matches.append({
                "id": job[0],
                "job_title": job[1],
                "description": job[2],
                "similarity": float(similarity)  # Convert for JSON
            })
        matches.sort(key=lambda x: x["similarity"], reverse=True)  # Highest first
        return matches[:5]  # Return top 5 matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)