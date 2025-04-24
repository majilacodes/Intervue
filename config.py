import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDvpOmdzcaLw1NIRtsNu1blC60-MLAUDO8')