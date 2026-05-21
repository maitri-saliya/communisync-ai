import requests
import json

def classify_issue(message):

    prompt = f'''
    Categorize this community issue.

    Message: {message}

    Return:
    Category
    Priority
    Assigned Team
    '''

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"]

    return result