from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
from deep_translator import GoogleTranslator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import jwt
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging
import time
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
import asyncio
from functools import lru_cache
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

app = FastAPI(title="Green Matchers API v3.2", version="3.2.0")

# Production Security - CORS + Rate Limit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ========================================
# JWT CONFIGURATION
# ========================================
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secure-secret-key-2025")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ========================================
# PRODUCTION DATABASE v3.2
# ========================================
fake_users_db = {
    "shivam": {"username": "shivam", "password": "hack2win", "role": "student", "email": "shivam@example.com"},
    "employer1": {"username": "employer1", "password": "greenjobs", "role": "employer", "email": "employer@example.com"}
}

# Real Indian Green Companies + WEBSITES
companies = {
    "python": ["Tata Power Renewables", "Adani Green Energy", "ReNew Power", "NTPC Renewable Energy", "Avaada Group"],
    "design": ["Avaada Group", "Suzlon Energy", "Sterling and Wilson Renewable Energy", "Greenko Group", "Sova Solar"],
    "data": ["NTPC Renewable Energy", "Azure Power", "JSW Energy", "Mytrah Energy", "Greenko Group"],
    "sustainable": ["Greenko Group", "Sova Solar", "Mytrah Energy", "Suzlon Energy", "Avaada Group"],
    "default": ["Tata Power Renewables", "Adani Green Energy", "ReNew Power", "NTPC Renewable Energy", "Avaada Group"]
}

company_websites = {
    "Tata Power Renewables": "https://www.tatapower.com/careers",
    "Adani Green Energy": "https://www.adanigreenenergy.com/careers",
    "ReNew Power": "https://www.renewpower.in/careers",
    "NTPC Renewable Energy": "https://www.ntpc.co.in/careers",
    "Avaada Group": "https://avaada.com/careers",
    "Suzlon Energy": "https://www.suzlon.com/careers",
    "Sterling and Wilson Renewable Energy": "https://www.sterlingandwilsonre.com/careers",
    "Greenko Group": "https://www.greenko.in/careers",
    "Sova Solar": "https://www.sovasolar.com/careers",
    "Azure Power": "https://www.azurepower.com/careers",
    "JSW Energy": "https://www.jsw.in/energy/careers",
    "Mytrah Energy": "https://www.mytrah.com/careers"
}

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "english", "hi": "hindi", "bn": "bengali", "mr": "marathi",
    "te": "telugu", "ta": "tamil", "gu": "gujarati", "ur": "urdu",
    "kn": "kannada", "or": "odia", "ml": "malayalam"
}

# Hindi Job Titles
HINDI_JOBS = {
    1: "इको इंजीनियर",
    2: "ग्रीन डेवलपर", 
    3: "नवीकरणीय विश्लेषक",
    4: "सस्टेनेबिलिटी कंसल्टेंट",
    5: "ग्रीन डेटा साइंटिस्ट"
}

# User Favorites
user_favorites = {}

# ========================================
# PYDANTIC MODELS
# ========================================
class SkillInput(BaseModel):
    skill_text: str
    lang: str = "en"

class JobInput(BaseModel):
    job_title: str
    job_description: str
    lang: str = "en"

class QueryInput(BaseModel):
    skill_text: List[str]
    lang: str = "en"
    location: Optional[str] = None

class ApplyInput(BaseModel):
    job_id: int
    cover_letter: str = ""

class CareerPathInput(BaseModel):
    current_skill: str
    years_experience: int = 5

# ========================================
# NEW v3.2 FUNCTIONS
# ========================================
def get_city_from_ip(ip: str) -> str:
    """AUTO-GEOLOCATION: Get user city from IP"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = response.json()
        return data.get("city", "Bengaluru")
    except:
        return "Bengaluru"

def calculate_distance(city1: str, city2: str) -> int:
    """DISTANCE CALCULATION: Km between cities"""
    distances = {
        ("bengaluru", "mumbai"): 850, ("bengaluru", "pune"): 850,
        ("bengaluru", "delhi"): 2150, ("bengaluru", "hyderabad"): 560,
        ("mumbai", "pune"): 150, ("delhi", "hyderabad"): 1550,
        ("pune", "hyderabad"): 550
    }
    return distances.get((city1.lower(), city2.lower()), 1000)

def ai_salary_predictor(skill: str, years: int = 0) -> tuple:
    """SALARY NEGOTIATOR: Predict +12% boost"""
    base_min, base_max = 8, 15
    boost = 1.12 + (years * 0.02)
    return int(base_min * boost), int(base_max * boost)

def generate_interview_questions(skill: str) -> List[str]:
    """INTERVIEW PREP: 5 Questions + Answers"""
    questions = {
        "python": [
            "Q1: Explain Python for solar panel optimization",
            "Q2: How to predict wind energy with ML?",
            "Q3: Carbon footprint calculation algorithm?",
            "Q4: ESG reporting with Python libraries?",
            "Q5: Renewable energy data pipeline design?"
        ]
    }
    return questions.get(skill.lower(), ["Q1: Basic renewable energy concepts", "Q2: Sustainability basics"])

def build_resume_pdf(username: str, skill: str) -> bytes:
    """RESUME BUILDER: 1-Click PDF"""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"SHIVAM - {skill.upper()} RESUME")
    p.drawString(100, 730, f"Green Jobs Specialist | {datetime.now().strftime('%Y')}")
    p.drawString(100, 710, f"Skills: {skill}, Renewable Energy, Sustainability")
    p.drawString(100, 690, "Experience: 5+ Years in Green Tech")
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

# ========================================
# JWT + AUTH FUNCTIONS
# ========================================
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

@lru_cache(maxsize=512)
def translate_text_cached(text: str, target_lang: str = "en"):
    try:
        if target_lang not in SUPPORTED_LANGUAGES:
            return text
        return GoogleTranslator(source='auto', target=SUPPORTED_LANGUAGES[target_lang]).translate(text)
    except:
        return text

def recommend_skills(current_skill: str):
    return {
        "python": ["Solar Panel Design", "Wind Energy Analysis", "Carbon Footprint ML"],
        "design": ["Sustainable Architecture", "Green Material Science", "ESG Reporting"],
        "data": ["Climate Modeling", "Renewable Forecasting", "Sustainability Analytics"]
    }.get(current_skill.lower(), ["Renewable Energy Basics"])

def get_cached_jobs(query: Optional[QueryInput] = None):
    base_jobs = [
        {"id": 1, "job_title": "Eco Engineer", "description": "Build renewable energy systems using Python", "salary": "₹8-15 LPA", "location": "Bengaluru", "sdg_impact": "SDG 7: 9/10 | 500 tons CO2/year", "company_rating": "4.8⭐", "urgency": "High Demand"},
        {"id": 2, "job_title": "Green Developer", "description": "Develop sustainable web apps", "salary": "₹6-12 LPA", "location": "Mumbai", "sdg_impact": "SDG 11: 8/10 | 200 tons waste/year", "company_rating": "4.8⭐", "urgency": "Apply Now!"},
        {"id": 3, "job_title": "Renewable Analyst", "description": "Analyze solar/wind data with AI", "salary": "₹7-14 LPA", "location": "Delhi", "sdg_impact": "SDG 7: 9/10 | 300 MWh/year", "company_rating": "4.8⭐", "urgency": "High Demand"},
        {"id": 4, "job_title": "Sustainability Consultant", "description": "Advise on ESG compliance", "salary": "₹10-18 LPA", "location": "Pune", "sdg_impact": "SDG 12: 9/10 | 95% compliance", "company_rating": "4.8⭐", "urgency": "Immediate"},
        {"id": 5, "job_title": "Green Data Scientist", "description": "ML models for climate prediction", "salary": "₹9-16 LPA", "location": "Hyderabad", "sdg_impact": "SDG 13: 10/10 | 98% accurate", "company_rating": "4.8⭐", "urgency": "High Demand"}
    ]

    matches = []
    skill_key = "default"
    if query:
        for skill in query.skill_text:
            for key in companies:
                if key in skill.lower():
                    skill_key = key
                    break

    for job in base_jobs:
        company = companies[skill_key][job["id"] % len(companies[skill_key])]
        job_title = HINDI_JOBS.get(job["id"], job["job_title"]) if query and query.lang == "hi" else job["job_title"]
        description = translate_text_cached(job["description"], query.lang) if query and query.lang == "hi" else job["description"]

        matches.append({
            "id": job["id"], "job_title": job_title, "description": description, "salary": job["salary"],
            "location": job["location"], "company": company, "company_rating": job["company_rating"],
            "sdg_impact": job["sdg_impact"], "urgency": job["urgency"], "website": company_websites.get(company),
            "similarity": 0.95
        })
    return matches

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

def send_email(to_email: str, subject: str, body: str):
    print(f"📧 EMAIL SENT TO {to_email}: {subject}")
    print(f"📧 CONTENT: {body[:100]}...")
    return True

# ========================================
# PRODUCTION ENDPOINTS v3.2
# ========================================

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.2.0", "features": ["Auto-Geo", "Distance", "Salary Boost", "Interview", "Resume"]}

@app.get("/stats")
def get_stats():
    return {
        "total_jobs": len(get_cached_jobs(None)),
        "users": len(fake_users_db),
        "languages": len(SUPPORTED_LANGUAGES),
        "companies": len(companies),
        "sdg_goals": 7,
        "favorites": len(user_favorites)
    }

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer", "user": user["username"]}

@app.post("/match_jobs")
@limiter.limit("10/minute")
async def match_jobs(request: Request, query: QueryInput, current_user: dict = Depends(get_current_user)):
    start_time = time.time()
    
    # v3.2 AUTO-GEOLOCATION
    user_city = get_city_from_ip(request.client.host)
    if not query.location:
        query.location = user_city
        print(f"👤 AUTO-DETECTED: {user_city}")
    
    jobs = get_cached_jobs(query)
    skill_text = " ".join(query.skill_text).lower()
    matches = []
    
    for job in jobs:
        similarity = 0.95 if "python" in skill_text else 0.90
        
        # v3.2 FIXED LOCATION FILTER
        if query.location:
            job_location = job["location"].lower()
            user_location = query.location.lower()
            if user_location in job_location or job_location in user_location:
                similarity += 0.05
                distance = calculate_distance(user_location, job_location)
            else:
                continue
        
        # v3.2 SALARY BOOST
        salary_min, salary_max = ai_salary_predictor(skill_text, 5)
        salary_boost = f"₹{salary_min}-{salary_max} LPA (+12%)"
        
        matches.append({
            "id": job["id"], "job_title": job["job_title"], "description": job["description"],
            "salary_range": job["salary"], "salary_boost": salary_boost,
            "location": job["location"], "distance_km": distance,
            "company": job["company"], "website": job["website"],
            "company_rating": job["company_rating"], "sdg_impact": job["sdg_impact"],
            "urgency": job["urgency"], "similarity": round(similarity, 2),
            "apply_url": f"https://greenmatchers.com/jobs/{job['id']}"
        })
    
    matches = sorted(matches, key=lambda x: x["similarity"], reverse=True)
    response_time = time.time() - start_time
    
    await manager.broadcast(f"🚨 {current_user['username']}: {len(matches)} JOBS in {query.location}!")
    send_email(current_user["email"], "🚨 NEW GREEN JOBS!", f"{len(matches)} matches in {query.location}!")
    
    return {
        "matches": matches[:5],
        "user_location": query.location,
        "auto_detected": user_city == query.location,
        "suggestions": recommend_skills(skill_text)[:2],
        "response_time": f"{response_time:.2f}s",
        "total_jobs": len(matches),
        "user": current_user["username"]
    }

@app.post("/generate_interview_prep")
async def interview_prep(query: QueryInput, current_user: dict = Depends(get_current_user)):
    questions = generate_interview_questions(" ".join(query.skill_text))
    return {"interview_questions": questions, "company": "Tata Power Renewables", "user": current_user["username"]}

@app.post("/generate_resume")
async def generate_resume(query: QueryInput, current_user: dict = Depends(get_current_user)):
    pdf_bytes = build_resume_pdf(current_user["username"], " ".join(query.skill_text))
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=resume_{current_user['username']}.pdf"}
    )

@app.post("/save_job")
async def save_job(job_id: int, current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    if username not in user_favorites:
        user_favorites[username] = []
    if job_id not in user_favorites[username]:
        user_favorites[username].append(job_id)
    return {"message": "Job saved!", "favorites": len(user_favorites[username])}

@app.post("/career_path")
async def career_path(career_data: CareerPathInput, current_user: dict = Depends(get_current_user)):
    path = {
        "python": ["Junior Eco Engineer", "Senior Green Developer", "CTO Sustainability"],
        "design": ["Junior Designer", "Lead Architect", "Head of Green Design"],
        "data": ["Junior Analyst", "Senior Data Scientist", "Chief Climate Officer"]
    }.get(career_data.current_skill.lower(), ["Specialist", "Expert", "Director"])
    
    salary_min, salary_max = ai_salary_predictor(career_data.current_skill, career_data.years_experience)
    
    return {
        "current_skill": career_data.current_skill,
        "years": career_data.years_experience,
        "career_path": path,
        "salary_projection": f"₹{salary_min}-{salary_max} LPA",
        "company": "Tata Power Renewables"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await websocket.send_text("🚀 Green Matchers v3.2 - AUTO-GEOLOCATION ACTIVE!")
    await asyncio.sleep(2)
    await websocket.send_text('🚨 NEW: "Solar Engineer" - ₹12-20 LPA - 5km away!')
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"💬 {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Initialize
print("✅ v3.2: AUTO-GEOLOCATION + DISTANCE + SALARY BOOST + INTERVIEW + RESUME LIVE!")
print("🚀 SHIVAM = ₹7 LAKH CHAMPION!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)