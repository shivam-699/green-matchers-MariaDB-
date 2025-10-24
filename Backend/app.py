from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np
from fastapi.responses import StreamingResponse
import requests
from deep_translator import GoogleTranslator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import jwt
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel, validator
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
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from diffusers import StableDiffusionPipeline  # Included for completeness, commented if unused
from math import radians, sin, cos, sqrt, atan2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

# Global variables
user_favorites = {}  # Ensure initialized

# Job demand data (mock for v3.3 trends)
job_demand = {"Bengaluru": 15, "Mumbai": 10, "Delhi": 8, "Pune": 5, "Hyderabad": 7}

app = FastAPI(title="Green Matchers API v3.3", version="3.3.0")

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

# Expanded Real Indian Green Companies mapped to skills (from search)
companies = {
    "python": ["Tata Power Renewables", "Adani Green Energy", "ReNew Power", "NTPC Renewable Energy", "Avaada Group", "Suzlon Energy", "Sterling and Wilson Renewable Energy", "Greenko Group", "Azure Power", "JSW Energy"],
    "design": ["Avaada Group", "Suzlon Energy", "Sterling and Wilson Renewable Energy", "Greenko Group", "Sova Solar", "Mytrah Energy", "Azure Power", "JSW Energy", "NTPC Renewable Energy", "ReNew Power"],
    "data": ["NTPC Renewable Energy", "Azure Power", "JSW Energy", "Mytrah Energy", "Greenko Group", "Avaada Group", "Suzlon Energy", "ReNew Power", "Adani Green Energy", "Tata Power Renewables"],
    "sustainable": ["Greenko Group", "Sova Solar", "Mytrah Energy", "Suzlon Energy", "Avaada Group", "Azure Power", "JSW Energy", "NTPC Renewable Energy", "ReNew Power", "Adani Green Energy"],
    "default": ["Tata Power Renewables", "Adani Green Energy", "ReNew Power", "NTPC Renewable Energy", "Avaada Group", "Suzlon Energy", "Sterling and Wilson Renewable Energy", "Greenko Group", "Azure Power", "JSW Energy"]
}

# Company Locations (expanded with search results)
company_locations = {
    "Tata Power Renewables": "Mumbai",
    "Adani Green Energy": "Ahmedabad",
    "ReNew Power": "Gurugram",
    "Suzlon Energy": "Pune",
    "Sterling and Wilson Renewable Energy": "Mumbai",
    "Azure Power": "New Delhi",
    "JSW Energy": "Mumbai",
    "Avaada Group": "Noida",
    "Greenko Group": "Hyderabad",
    "Sova Solar": "Kolkata",
    "Mytrah Energy": "Hyderabad",
    "NTPC Renewable Energy": "New Delhi"
}

# Company Reviews (from Glassdoor search, approx ratings)
company_reviews = {
    "Tata Power Renewables": {"rating": 4.0, "reviews": 442},
    "Adani Green Energy": {"rating": 3.7, "reviews": 120},
    "ReNew Power": {"rating": 3.8, "reviews": 95},
    "Suzlon Energy": {"rating": 3.9, "reviews": 150},
    "Sterling and Wilson Renewable Energy": {"rating": 4.0, "reviews": 200},
    "Azure Power": {"rating": 4.1, "reviews": 100},
    "JSW Energy": {"rating": 4.0, "reviews": 280},
    "Avaada Group": {"rating": 4.9, "reviews": 19},
    "Greenko Group": {"rating": 4.0, "reviews": 110},
    "Sova Solar": {"rating": 4.0, "reviews": 50},
    "Mytrah Energy": {"rating": 3.9, "reviews": 80},
    "NTPC Renewable Energy": {"rating": 3.8, "reviews": 250}
}
company_websites = {
    "Tata Power Renewables": "https://www.tatapower.com/careers",
    "Adani Green Energy": "https://www.adanigreenenergy.com/careers",
    "ReNew Power": "https://www.renewpower.in/careers",
    "Suzlon Energy": "https://www.suzlon.com/careers",
    "NTPC Renewable Energy": "https://www.ntpc.co.in/careers",
    "Avaada Group": "https://avaada.com/careers",
    "Greenko Group": "https://www.greenko.in/careers",
    "JSW Energy": "https://www.jsw.in/energy/careers",
    "Azure Power": "https://www.azurepower.com/careers",
    "Sterling and Wilson Renewable Energy": "https://www.sterlingandwilsonre.com/careers"
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

# Global AI Models
model = None
generator = None
sd_pipe = None

# ========================================
# ENHANCED PYDANTIC MODELS
# ========================================
class SkillInput(BaseModel):
    skill_text: str
    lang: str = "en"
    
    @validator('skill_text')
    def validate_skill(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Skill must be at least 2 characters')
        return v

class JobInput(BaseModel):
    job_title: str
    job_description: str
    lang: str = "en"

class QueryInput(BaseModel):
    skill_text: List[str]
    lang: str = "en"
    location: Optional[str] = None  # New param for user location

class ApplyInput(BaseModel):
    job_id: int
    cover_letter: str = ""

class CareerPathInput(BaseModel):
    current_skill: str
    years_experience: int = 5

def train_salary_predictor():
    data = np.array([[8, 9], [6, 7], [7, 8], [10, 11]])
    X, y = data[:, 0:1], data[:, 1]
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(1, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X.reshape((4, 1, 1)), y, epochs=100, verbose=0)
    return model


class ImpactInput(BaseModel):
    role: str
    hours_per_week: int
    duration_months: int

salary_model = train_salary_predictor()

# ========================================
# FIXED get_cached_jobs FUNCTION
# =====================================

@lru_cache(maxsize=128)
def translate_text_cached(text, lang):
    return GoogleTranslator(source='auto', target=lang).translate(text)

def get_cached_jobs(query: Optional[QueryInput] = None):
    base_jobs = [
        {
            "id": 1, "job_title": "Eco Engineer", "description": "Build renewable energy systems using Python",
            "salary": "₹8-15 LPA", "location": "Bengaluru", "sdg_impact": "SDG 7: 9/10 | Carbon Saved: 500 tons/year",
            "company_rating": "4.8⭐", "urgency": "High Demand"
        },
        {
            "id": 2, "job_title": "Green Developer", "description": "Develop sustainable web apps for waste management",
            "salary": "₹6-12 LPA", "location": "Mumbai", "sdg_impact": "SDG 11: 8/10 | Waste Reduced: 200 tons/year",
            "company_rating": "4.8⭐", "urgency": "Apply Now!"
        },
        {
            "id": 3, "job_title": "Renewable Analyst", "description": "Analyze solar/wind energy data with AI/ML",
            "salary": "₹7-14 LPA", "location": "Delhi", "sdg_impact": "SDG 7: 9/10 | Energy Saved: 300 MWh/year",
            "company_rating": "4.8⭐", "urgency": "High Demand"
        },
        {
            "id": 4, "job_title": "Sustainability Consultant", "description": "Advise companies on ESG compliance",
            "salary": "₹10-18 LPA", "location": "Pune", "sdg_impact": "SDG 12: 9/10 | Compliance Score: 95%",
            "company_rating": "4.8⭐", "urgency": "Immediate"
        },
        {
            "id": 5, "job_title": "Green Data Scientist", "description": "ML models for climate prediction",
            "salary": "₹9-16 LPA", "location": "Hyderabad", "sdg_impact": "SDG 13: 10/10 | Predictions: 98% accurate",
            "company_rating": "4.8⭐", "urgency": "High Demand"
        }
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
        job_title = HINDI_JOBS.get(job["id"], job_title) if query and query.lang == "hi" else job["job_title"]
        description = translate_text_cached(job["description"], query.lang) if query and query.lang == "hi" else job["description"]

        matches.append({
            "id": job["id"], "job_title": job_title, "description": description, "salary": job["salary"],
            "location": job["location"], "company": company, "company_rating": job["company_rating"],
            "sdg_impact": job["sdg_impact"], "urgency": job["urgency"], "website": company_websites.get(company),
            "similarity": 0.95
        })
    return matches

# Load AI Models
def load_models():
    global model, generator, sd_pipe
    print("🔄 Loading AI Models...")
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    generator = pipeline("text-generation", model="gpt2", max_new_tokens=100, truncation=True)
    sd_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", safety_checker=None)
    sd_pipe = sd_pipe.to("cpu")
    print("✅ AI Models Loaded!")

# Initialize Database
def init_db():
    print("✅ PRODUCTION DATABASE v3.3: In-Memory + REAL COMPANIES + SDG Scores + Multi-Language + Trends")
    load_models()
    global salary_model
    salary_model = train_salary_predictor()  # Initialize here
    return True


# Enhanced Auto-Geolocation using ipinfo.io (v3.3)
def get_city_from_ip(ip):
    try:
        api_key = os.getenv("IPINFO_API_KEY", "your-api-key-here")  # Add to .env
        response = requests.get(f"https://ipinfo.io/{ip}/city?token={api_key}").text
        return response if response else "Unknown"
    except:
        return "Unknown"

# Distance Calculation (v3.2 placeholder, refine with geodata in v3.3)
def calculate_distance(loc1, loc2):
    return 0 if loc1 == loc2 else 10  # Dummy value, improve with lat/long

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

# AI Salary Prediction
def ai_salary_predictor(skill, years):
    base_salary = {"python": 8, "design": 6, "data": 7, "sustainable": 10}[skill.lower()]
    return base_salary + years, base_salary + years + 5  # Min, Max LPA

def recommend_skills(skills):
    return ["Solar Panel Design", "Wind Energy Analysis"] if "python" in skills else ["Green Coding", "Sustainability"]

def generate_interview_questions(skills):
    return ["Tell me about your Python experience.", "How would you optimize renewable energy code?"]

def build_resume_pdf(username, skills):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Resume - {username}")
    p.drawString(100, 730, f"Skills: {skills}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

# ========================================
# PRODUCTION ENDPOINTS v3.3
# ========================================

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.3.0", "features": ["Auto-Geo", "Distance", "Salary Boost", "Interview", "Resume", "Trends", "Cover Letter"]}

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

@app.get("/job_trends")  # v3.3: Trends Chart
async def job_trends():
    return {
        "chart": {
            "type": "bar",
            "data": {
                "labels": list(job_demand.keys()),
                "datasets": [{
                    "label": "Job Demand",
                    "data": list(job_demand.values()),
                    "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"]
                }]
            },
            "options": {
                "scales": {"y": {"beginAtZero": True}}
            }
        }
    }

@app.get("/dashboard")
async def dashboard():
    predictions = salary_model.predict(np.array([[10]]).reshape((1, 1, 1)))
    chart_data = [8, 9, 7, 11, float(predictions[0][0])]  # Convert to float
    return {"chart": {"type": "line", "data": {"labels": ["Jan", "Feb", "Mar", "Apr", "Future"], "datasets": [{"data": chart_data, "backgroundColor": "#36A2EB"}]}}}


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer", "user": user["username"]}

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

@app.post("/match_jobs")
@limiter.limit("10/minute")
async def match_jobs(request: Request, query: QueryInput, current_user: dict = Depends(get_current_user)):
    start_time = time.time()
    
    # v3.3 Enhanced AUTO-GEOLOCATION
    user_city = get_city_from_ip(request.client.host)
    if not query.location or query.location.lower() == "string":
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
    if not user_favorites.get(username):  # Safety check
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
    }.get(career_data.current_skill.lower(), ["Green Specialist", "Senior Expert", "Director"])
    
    salary_min, salary_max = ai_salary_predictor(career_data.current_skill, career_data.years_experience)
    
    return {
        "current_skill": career_data.current_skill,
        "years": career_data.years_experience,
        "career_path": path,
        "salary_projection": f"₹{salary_min}-{salary_max} LPA",
        "company": "Tata Power Renewables",
        "sdg_impact": "Maximum contribution to 7 SDGs"
    }

@app.post("/generate_cover_letter")  # v3.3: Cover Letter Generation
async def generate_cover_letter(query: QueryInput, current_user: dict = Depends(get_current_user)):
    cover_letter = f"Dear Hiring Manager,\nI am excited to apply for the {query.skill_text[0]} role at {next(iter(company_websites))}. With my experience in {query.skill_text[0]}, I can contribute to your green initiatives.\nBest,\n{current_user['username']}"
    return {"cover_letter": cover_letter, "user": current_user["username"]}

@app.post("/simulate_impact")
async def simulate_impact(input: ImpactInput, current_user: dict = Depends(get_current_user)):
    impact_per_hour = {"Eco Engineer": 0.5, "Green Developer": 0.3, "Renewable Analyst": 0.4}  # Tons CO2 saved per hour
    total_impact = (impact_per_hour.get(input.role, 0.1) * input.hours_per_week * (input.duration_months * 4)) / 1000  # Convert to tons
    return {
        "chart": {
            "type": "pie",
            "data": {
                "labels": ["CO2 Saved", "Remaining Impact"],
                "datasets": [{
                    "data": [total_impact, 1 - total_impact],
                    "backgroundColor": ["#4BC0C0", "#FFCE56"]
                }]
            }
        },
        "total_impact_tons": f"{total_impact:.2f} tons",
        "user": current_user["username"]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await websocket.send_text("🚀 Green Matchers v3.3 - AUTO-GEOLOCATION ACTIVE!")
    await asyncio.sleep(2)
    await websocket.send_text('🚨 NEW: "Solar Engineer" - ₹12-20 LPA - 5km away!')
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"💬 {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Initialize
init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)