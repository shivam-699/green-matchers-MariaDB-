from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Application(db.Model):
    __tablename__ = 'applications'
    
    application_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), nullable=False)
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.String(500))
    status = db.Column(db.Enum('applied', 'viewed', 'shortlisted', 'rejected', 'hired'), default='applied')
    applied_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('applications', lazy=True))
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))

class EmployerProfile(db.Model):
    __tablename__ = 'employer_profiles'
    
    employer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    position = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('employer_profile', uselist=False))
    company = db.relationship('Company', backref=db.backref('employers', lazy=True))

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    headline = db.Column(db.String(200))
    summary = db.Column(db.Text)
    phone_number = db.Column(db.String(15))
    current_salary = db.Column(db.Numeric(10, 2))
    expected_salary = db.Column(db.Numeric(10, 2))
    notice_period = db.Column(db.Integer)
    resume_url = db.Column(db.String(500))
    linkedin_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    portfolio_url = db.Column(db.String(200))
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('profile', uselist=False))

class UserEducation(db.Model):
    __tablename__ = 'user_education'
    
    education_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    field_of_study = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    grade = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('education', lazy=True))

class UserExperience(db.Model):
    __tablename__ = 'user_experience'
    
    experience_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    current_job = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('experience', lazy=True))

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum('application', 'job_alert', 'system', 'message'), default='system')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))

class SavedSearch(db.Model):
    __tablename__ = 'saved_searches'
    
    search_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    search_name = db.Column(db.String(100))
    search_query = db.Column(db.JSON)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('saved_searches', lazy=True))

# Update existing User model (add to your existing User class)
# Add these fields to your existing User model:
# phone_number = db.Column(db.String(15))
# is_verified = db.Column(db.Boolean, default=False)
# last_login = db.Column(db.TIMESTAMP)