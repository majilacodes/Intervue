# AI Interview Platform

A Flask-based application that uses Google's Gemini API to create personalized mock interviews, evaluate responses, and provide detailed feedback.

## Features

- Create custom mock interviews for specific job roles
- AI-generated interview questions based on job description and requirements
- Audio recording and speech-to-text transcription
- Real-time feedback and evaluation from Gemini AI
- Score tracking and comprehensive analysis

## Screenshots

The interface is designed to be clean and minimal, focusing on functionality:

1. Landing page with an introduction to the platform
2. Dashboard to manage all mock interviews
3. Interview creation form with job details
4. Interactive interview page with webcam support
5. Detailed results page with feedback and comparison

## Prerequisites

- Python 3.7 or higher
- Flask
- Google Generative AI Python SDK
- SQLite (included with Python)
- Modern web browser with WebRTC support (for webcam/microphone)

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd interview-platform
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install Flask Flask-SQLAlchemy google-generativeai
   ```

5. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

## Running the Application

1. Make sure your virtual environment is activated

2. Set the Flask application:
   - On Windows:
     ```
     set FLASK_APP=app.py
     ```
   - On macOS/Linux:
     ```
     export FLASK_APP=app.py
     ```

3. Initialize the database (first time only):
   ```
   flask shell
   ```
   Then in the shell:
   ```python
   from app import db
   db.create_all()
   exit()
   ```

4. Run the application:
   ```
   flask run
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000/`

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Navigate to the API section
4. Create a new API key
5. Copy the key and add it to your `.env` file

## Project Structure

```
interview_platform/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database setup and models
├── helpers.py             # Helper functions
├── gemini_api.py          # Gemini API integration
│
├── static/
│   ├── css/
│   │   └── styles.css     # Custom styles
│   └── js/
│       ├── interview.js   # Interview page functionality
│       └── script.js      # General script
│
├── templates/
│   ├── landing.html       # Landing page
│   ├── home.html          # Dashboard with mock interviews
│   ├── create.html        # Create new interview
│   ├── interview.html     # Interview questions and answers
│   ├── result.html        # Results and feedback
│   └── layout.html        # Base template
│
└── instance/
    └── interviews.db      # SQLite database
```

## Limitations

This is a Minimum Viable Product (MVP) with basic functionality. Some limitations include:

- Basic speech-to-text functionality using browser APIs (may vary in accuracy)
- Limited formatting and styling
- No user authentication system
- Simplified error handling
- No persistent storage for video/audio

## Extending the Application

You can extend this application by:

1. Adding user authentication
2. Implementing more sophisticated speech-to-text
3. Adding a more comprehensive question bank
4. Implementing industry-specific templates
5. Adding interview time limits and progress tracking

## License

This project is licensed under the MIT License - see the LICENSE file for details.