from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import db, Interview, Question
from gemini_api import generate_interview_questions, evaluate_answer
import os
from config import SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize database
db.init_app(app)

# Create tables within app context instead of using before_first_request
with app.app_context():
    db.create_all()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
def home():
    interviews = Interview.query.order_by(Interview.created_at.desc()).all()
    return render_template('home.html', interviews=interviews)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        job_role = request.form.get('job_role')
        job_description = request.form.get('job_description')
        years_experience = request.form.get('years_experience')
        tech_stack = request.form.get('tech_stack')
        
        # Create new interview
        new_interview = Interview(
            job_role=job_role,
            job_description=job_description,
            years_experience=years_experience,
            tech_stack=tech_stack
        )
        db.session.add(new_interview)
        db.session.commit()
        
        # Generate questions using Gemini API
        questions = generate_interview_questions(
            job_role, job_description, years_experience, tech_stack
        )
        
        # Add questions to database
        for i, question_text in enumerate(questions, 1):
            question = Question(
                interview_id=new_interview.id,
                question_text=question_text,
                position=i
            )
            db.session.add(question)
        
        db.session.commit()
        
        return redirect(url_for('interview', interview_id=new_interview.id, question_num=1))
    
    return render_template('create.html')

@app.route('/interview/<int:interview_id>/question/<int:question_num>', methods=['GET', 'POST'])
def interview(interview_id, question_num):
    interview = Interview.query.get_or_404(interview_id)
    question = Question.query.filter_by(interview_id=interview_id, position=question_num).first_or_404()
    
    total_questions = 5  # Fixed number of questions
    
    if request.method == 'POST':
        # Save the answer
        question.user_answer = request.form.get('answer', '')
        db.session.commit()
        
        if question_num < total_questions:
            # Proceed to next question
            return redirect(url_for('interview', interview_id=interview_id, question_num=question_num+1))
        else:
            # All questions answered, redirect to evaluation
            return redirect(url_for('evaluate', interview_id=interview_id))
    
    return render_template('interview.html', interview=interview, question=question, 
                           question_num=question_num, total_questions=total_questions)

@app.route('/interview/<int:interview_id>/save_answer', methods=['POST'])
def save_answer(interview_id):
    """Save transcribed answer via AJAX"""
    question_num = request.json.get('question_num')
    answer_text = request.json.get('answer_text')
    
    question = Question.query.filter_by(interview_id=interview_id, position=question_num).first_or_404()
    question.user_answer = answer_text
    db.session.commit()
    
    return jsonify({"success": True})

@app.route('/interview/<int:interview_id>/evaluate')
def evaluate(interview_id):
    """Process evaluation of all questions"""
    interview = Interview.query.get_or_404(interview_id)
    questions = Question.query.filter_by(interview_id=interview_id).order_by(Question.position).all()
    
    total_score = 0
    
    # Evaluate each answer
    for question in questions:
        if question.user_answer:
            evaluation = evaluate_answer(question.question_text, question.user_answer, interview.job_role)
            question.expected_answer = evaluation['expected_answer']
            question.feedback = evaluation['feedback']
            question.score = evaluation['score']
            total_score += evaluation['score']
    
    # Calculate overall score
    if questions:
        interview.overall_score = total_score / len(questions)
    
    db.session.commit()
    
    return redirect(url_for('result', interview_id=interview_id))

@app.route('/interview/<int:interview_id>/result')
def result(interview_id):
    """Show results page"""
    interview = Interview.query.get_or_404(interview_id)
    questions = Question.query.filter_by(interview_id=interview_id).order_by(Question.position).all()
    
    return render_template('result.html', interview=interview, questions=questions)

@app.route('/about')
def about():
    """Show About Us page"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Show Services page"""
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Show Contact Us page and handle form submission"""
    if request.method == 'POST':
        # Here you would typically handle the form submission
        # For now, we'll just redirect back to the contact page
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)