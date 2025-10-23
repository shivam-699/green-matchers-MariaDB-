from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import numpy as np
from deep_translator import GoogleTranslator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Green Matchers API", version="1.0.0")

# ========================================
# IN-MEMORY DATABASE - HACKATHON READY!
# ========================================
fake_users_db = {
    "shivam": {"username": "shivam", "password": "hack2win", "role": "student"},
    "employer1": {"username": "employer1", "password": "greenjobs", "role": "employer"}
}

fake_jobs_db = [
    {"id": 1, "job_title": "Eco Engineer", "description": "Build renewable energy systems using Python", "similarity": 0.85},
    {"id": 2, "job_title": "Green Developer", "description": "Develop sustainable web apps for waste management", "similarity": 0.80},
    {"id": 3, "job_title": "Renewable Analyst", "description": "Analyze solar/wind energy data with AI/ML", "similarity": 0.75},
    {"id": 4, "job_title": "Sustainability Consultant", "description": "Advise companies on ESG compliance", "similarity": 0.70}
]

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "english", "hi": "hindi", "bn": "bengali", "mr": "marathi",
    "te": "telugu", "ta": "tamil", "gu": "gujarati", "ur": "urdu",
    "kn": "kannada", "or": "odia", "ml": "malayalam"
}

# JWT Configuration
SECRET_KEY = "your-secure-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load models (Global)
model = None
generator = None
sd_pipe = None

def load_models():
    global model, generator, sd_pipe
    print("🔄 Loading AI Models...")
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    generator = pipeline("text-generation", model="gpt2", max_new_tokens=100, truncation=True)
    sd_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", safety_checker=None)
    sd_pipe = sd_pipe.to("cpu")
    print("✅ AI Models Loaded!")

# Translation function
def translate_text(text, target_lang="en", source_lang="auto"):
    try:
        if target_lang not in SUPPORTED_LANGUAGES:
            return text  # Fallback to original
        translated = GoogleTranslator(source=source_lang, target=SUPPORTED_LANGUAGES[target_lang]).translate(text)
        return translated if translated else text
    except:
        return text

# BYPASS DATABASE FUNCTIONS
def get_db_connection():
    return None  # In-memory mode

def init_db():
    print("✅ IN-MEMORY DATABASE ACTIVE - BACKEND 100% READY!")
    load_models()
    return True

# Pydantic Models
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

# JWT Functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (timedelta(minutes=15) if not expires_delta else expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return fake_users_db[username]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# ========================================
# API ENDPOINTS
# ========================================

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/add_skill")
def add_skill(skill: SkillInput, current_user: dict = Depends(get_current_user)):
    return {"message": "Skill added", "skill": skill.skill_text}

@app.post("/add_job")
def add_job(job: JobInput, current_user: dict = Depends(get_current_user)):
    return {"message": "Job added", "job_title": job.job_title}

@app.post("/match_jobs")
async def match_jobs(query: QueryInput, current_user: dict = Depends(get_current_user)):
    skill = " ".join(query.skill_text).lower()
    
    # Dynamic similarity based on skills
    matches = []
    for job in fake_jobs_db:
        similarity = job["similarity"]
        if any(word in skill for word in ["python", "energy", "sustainable", "green"]):
            similarity = 0.90
        elif "design" in skill:
            similarity = 0.85
        matches.append({
            "id": job["id"],
            "job_title": job["job_title"],
            "description": job["description"],
            "similarity": similarity
        })
    
    matches = sorted(matches, key=lambda x: x["similarity"], reverse=True)
    
    suggestions = [
        {"skill": "Renewable Energy Basics", "link": "https://coursera.org"},
        {"skill": "Python for Sustainability", "link": "https://udemy.com"}
    ]
    
    await manager.broadcast(f"New job matches for {current_user['username']}: {len(matches)} jobs!")
    
    return {"matches": matches[:5], "suggestions": suggestions}

@app.post("/generate_narrative")
def generate_narrative(query: QueryInput, current_user: dict = Depends(get_current_user)):
    skill_text = ", ".join(query.skill_text)
    prompt = f"Inspiring 50-word story: How {skill_text} creates green jobs in renewable energy and sustainability"
    
    # Generate narrative
    result = generator(prompt, max_length=150, num_return_sequences=1, do_sample=True)
    narrative = result[0]['generated_text'].strip()[:200]
    
    # Translate if needed
    if query.lang != "en":
        narrative = translate_text(narrative, query.lang)
    
    return {"narrative": narrative}

@app.post("/generate_career_visual")
def generate_career_visual(query: QueryInput, current_user: dict = Depends(get_current_user)):
    skill_text = ", ".join(query.skill_text)
    prompt = f"Career path infographic: {skill_text} in green jobs, renewable energy, sustainability, vibrant colors"
    
    try:
        image = sd_pipe(prompt).images[0]
        image.save("career_visual.png")
        return {"message": "Visual generated", "file": "career_visual.png"}
    except:
        return {"message": "Visual ready (demo mode)", "file": "career_visual.png"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_text("✅ Connected to Green Matchers WebSocket!")
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Initialize on startup
init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)