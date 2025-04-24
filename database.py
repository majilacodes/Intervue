from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_role = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    years_experience = db.Column(db.String(50), nullable=True)
    tech_stack = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref='interview', lazy=True, cascade='all, delete-orphan')
    overall_score = db.Column(db.Float, nullable=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interview.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    user_answer = db.Column(db.Text, nullable=True)
    expected_answer = db.Column(db.Text, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    position = db.Column(db.Integer, nullable=False)  # Question number (1-5)