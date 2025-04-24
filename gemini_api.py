import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def get_model():
    """Returns the Gemini model"""
    # Updated to use the correct model name - Gemini 1.0 Pro
    return genai.GenerativeModel('gemini-2.0-flash')

def generate_interview_questions(job_role, job_description, years_experience, tech_stack):
    """Generate interview questions based on job details"""
    model = get_model()
    
    prompt = f"""
    Create 5 technical interview questions for a {job_role} position.
    
    Job Description: {job_description}
    Required Experience: {years_experience} years
    Technology Stack: {tech_stack}
    
    Format the questions as a list of 5 detailed, technical questions that would be asked in a real interview.
    Each question should:
    - Be at least 2 sentences long
    - Test specific technical knowledge relevant to the role
    - Include context or a scenario when appropriate
    - Be detailed and comprehensive enough to evaluate deep technical understanding
    - Challenge the candidate to demonstrate both theoretical knowledge and practical experience
    """
    
    response = model.generate_content(prompt)
    
    # Parse the response into a list of 5 questions
    questions_text = response.text
    questions = []
    
    # Simple parsing logic - improve as needed
    for line in questions_text.split('\n'):
        line = line.strip()
        if line and (line.startswith('Question') or line.startswith('1.') or 
                   line.startswith('2.') or line.startswith('3.') or 
                   line.startswith('4.') or line.startswith('5.')):
            # Remove the number/prefix
            if '.' in line:
                question = line.split('.', 1)[1].strip()
                questions.append(question)
            elif ':' in line:
                question = line.split(':', 1)[1].strip()
                questions.append(question)
    
    # Ensure we have exactly 5 questions
    if len(questions) < 5:
        # If parsing failed, just use the whole text split into 5 parts
        questions = questions_text.split('\n\n')[:5]
    
    return questions[:5]  # Return only first 5 questions

def evaluate_answer(question, user_answer, job_role):
    """Evaluate user's answer to an interview question"""
    model = get_model()
    
    prompt = f"""
    Evaluate this answer for a {job_role} interview question.
    
    Question: {question}
    
    User's Answer: {user_answer}
    
    Please provide:
    1. An expected answer that would be considered excellent (2-3 paragraphs)
    2. Specific feedback on the user's answer (strengths and areas for improvement)
    3. A score from 1 to 10 based on technical accuracy, completeness, and clarity
    
    Format your response as:
    Expected Answer: [your expected answer here]
    Feedback: [your feedback here]
    Score: [numeric score]
    """
    
    response = model.generate_content(prompt)
    response_text = response.text
    
    # Parse the response
    expected_answer = ""
    feedback = ""
    score = 0
    
    for line in response_text.split('\n'):
        if line.startswith('Expected Answer:'):
            expected_answer = line.replace('Expected Answer:', '').strip()
        elif line.startswith('Feedback:'):
            feedback = line.replace('Feedback:', '').strip()
        elif line.startswith('Score:'):
            try:
                score_text = line.replace('Score:', '').strip()
                score = float(score_text)
            except ValueError:
                score = 5.0  # Default score if parsing fails
    
    # If parsing fails, use simpler approach
    if not expected_answer:
        parts = response_text.split('\n\n')
        if len(parts) >= 3:
            expected_answer = parts[0]
            feedback = parts[1]
            try:
                score = float(parts[2].split()[-1])
            except (ValueError, IndexError):
                score = 5.0
    
    return {
        'expected_answer': expected_answer,
        'feedback': feedback,
        'score': score
    }