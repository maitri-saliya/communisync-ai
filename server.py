from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse

import requests

from database import SessionLocal
from models import Issue

app = FastAPI()


# ----------------------------------------
# AI CLASSIFICATION
# ----------------------------------------

# def classify_issue(message):

#     prompt = f"""
#     Analyze this community issue.

#     Return ONLY in this format:

#     Category: ...
#     Priority: ...
#     Assigned Team: ...

#     Message:
#     {message}
#     """

#     try:

#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "mistral",
#                 "prompt": prompt,
#                 "stream": False
#             }
#         )

#         result = response.json()["response"]

#         return result

#     except:

#         return """
# Category: Maintenance
# Priority: Medium
# Assigned Team: Civic Support Team
# """

def classify_issue(message):

    msg = message.lower()

    if "water" in msg:
        return """
Category: Emergency
Priority: High
Assigned Team: Utility Team
"""

    elif "light" in msg:
        return """
Category: Maintenance
Priority: Medium
Assigned Team: Civic Team
"""

    return """
Category: General
Priority: Low
Assigned Team: Community Team
"""


# ----------------------------------------
# EXTRACT AI FIELDS
# ----------------------------------------

def extract_field(text, field):

    try:

        for line in text.splitlines():

            if field.lower() in line.lower():

                return line.split(":")[1].strip()

    except:
        pass

    return "Unknown"


# ----------------------------------------
# WHATSAPP WEBHOOK
# ----------------------------------------

@app.post("/whatsapp")

async def whatsapp_reply(request: Request):

    form = await request.form()

    incoming_msg = form.get("Body")

    ai_result = classify_issue(incoming_msg)

    category = extract_field(ai_result, "Category")

    priority = extract_field(ai_result, "Priority")

    assigned_team = extract_field(
        ai_result,
        "Assigned Team"
    )

    # SAVE TO DATABASE

    db = SessionLocal()

    issue = Issue(
        message=incoming_msg,
        category=category,
        priority=priority,
        assigned_team=assigned_team,
        status="Pending"
    )

    db.add(issue)

    db.commit()

    db.close()

    # WHATSAPP RESPONSE

    response = MessagingResponse()

    response.message(
        f"""
CommuniSync AI Analysis

Category: {category}
Priority: {priority}
Assigned Team: {assigned_team}

Your request has been routed successfully.
"""
    )

    return str(response)