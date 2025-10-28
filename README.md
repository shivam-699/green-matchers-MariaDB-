# 🌿 Green Matchers - AI Powered Career Platform

> **Intelligent career matching for the modern workforce powered by AI**

[![React](https://img.shields.io/badge/React-18.2-blue)]()
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![MariaDB](https://img.shields.io/badge/Database-MariaDB-orange)]()
[![Vite](https://img.shields.io/badge/Build-Vite-purple)]()
[![Tailwind](https://img.shields.io/badge/Styling-Tailwind_CSS-38B2AC)]()

## 🎯 Problem Statement
Traditional career platforms fail to provide personalized, AI-driven career paths that adapt to individual skills and market demands in the green economy.

## 💡 Our Solution
Green Matchers uses advanced AI algorithms to:
- 🤖 Analyze user skills and preferences using AI
- 🎯 Match with ideal green career paths  
- 📊 Provide real-time market insights
- 📚 Offer personalized learning recommendations
- 🌱 Focus on sustainable and green jobs

## 🏗️ System Architecture
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Frontend        │ │     Backend      │ │     Database    │
│                 │ │                  │ │                 │
│  React + Vite  │◄─►│ FastAPI + Python │◄─►│   MariaDB    │
│                 | |                  | |                 |
|   Tailwind CSS  │ │    OpenAI API    │ │  Green Jobs     │
└─────────────────┘ └──────────────────┘ └─────────────────┘



## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Python 3.8+
- MariaDB Server
- npm

### Installation & Running

1. **Clone and setup**
```bash
git clone https://github.com/shivam-699/green-matchers-MariaDB-
cd green-matchers-MariaDB-
```

## Backend Setup (FastAPI)
cd Backend
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# Install dependencies
pip install -r requirements.txt
# Start backend server
uvicorn app:app --reload
Backend runs at: http://localhost:8000
API Docs: http://localhost:8000/docs



## Frontend Setup
cd Frontend
npm install
npm run dev
Frontend runs at: http://localhost:3000

## 📊 Database Schema (MariaDB)
Your MariaDB database contains:
51 companies in renewable energy sector
24 green job listings with detailed descriptions
4 users with skills and profiles
Job demand data across Indian cities
Favorites system for job tracking


## 📁 Project Structure
green-matchers-MariaDB-/
├── 📂 Backend/
│   ├── app.py                 # FastAPI main application
│   ├── requirements.txt       # Python dependencies
│   ├── .env                  # Environment variables
│   ├── green_jobs.db         # SQLite database
│   ├── career_visual.png     # Career visualization assets
│   └── test_connection.py    # Database connection tests
├── 📂 Frontend/
│   ├── src/                  # React components & pages
│   ├── package.json          # Frontend dependencies
│   ├── vite.config.js        # Vite configuration
│   ├── tailwind.config.js    # Tailwind CSS config
│   └── index.html            # Main HTML entry point
├── 📜 README.md              # This file
├── 📜 LICENSE               # MIT License
└── 📜 .gitignore            # Git ignore rules



## 🔌 API Endpoints
Method	    Endpoint        	  Description
GET	         /career-paths	     Get all career paths
POST	       /match-user	       Match user with careers
GET	         /user/{id}	         Get user profile
POST	       /analyze-skills	   AI skill analysis


## 🛠️ Tech Stack
Frontend: React, Vite, Tailwind CSS, Axios
Backend: FastAPI, Python, Uvicorn, SQLAlchemy
Database: MariaDB with 50+ companies & 24+ green jobs
AI/ML: OpenAI GPT API
Styling: Tailwind CSS, Responsive Design
Tools: Git, GitHub, Postman


## 🎯 Key Features
✅ AI-Powered Career Matching
✅ Real MariaDB Database with Real Data
✅ 50+ Green Energy Companies
✅ 24+ Detailed Job Listings
✅ User Profiles & Favorites System
✅ Responsive Web Interface
✅ RESTful API with Auto-docs


## 📈 Data Highlights
51 Companies: Solar, Wind, Bio-energy sectors
24 Green Jobs: From Junior to Executive levels
Multiple Locations: Pan-India job opportunities
SDG Alignment: All jobs mapped to UN Sustainable Development Goals
Salary Data: Realistic compensation ranges


## 👥 Team Members
Shivam - Full Stack Developer & Database Architect
Sakthi Bala Sundaram -
Nishani B -
Neha RN -
Nimalan -



## 🎥 Live Demo
Frontend Application: http://localhost:3000
Backend API Documentation: http://localhost:8000/docs
Career Path Page: http://localhost:3000/career-path

## 🔮 Future Enhancements
Advanced AI matching algorithms
User authentication system
Mobile application
Real-time notifications
Skill gap analysis
Job application tracking

## 📄 License
MIT License - see LICENSE file for details
