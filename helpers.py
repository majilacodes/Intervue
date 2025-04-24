from flask import session, redirect, url_for
from functools import wraps

def format_date(date):
    """Format date for display"""
    if date:
        return date.strftime("%B %d, %Y, %I:%M %p")
    return ""

def format_score(score):
    """Format score for display"""
    if score is None:
        return "N/A"
    return f"{score:.1f}/10"