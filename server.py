from fastapi import FastAPI, Request
from fastapi.responses import Response

import os

from openai import OpenAI

from database import SessionLocal
from models import Issue


# -----------------------------------
# APP
# -----------------------------------

app = FastAPI()


# -----------------------------------
# OPENAI CLIENT
# -----------------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# -----------------------------------
# AI CLASSIFICATION
# -----------------------------------

def classify_issue(message):

    prompt = f"""
You are CommuniSync AI.

Analyze the community request.

Return ONLY this format:

Category:
Priority:
Assigned Team:
Suggested Action:

Request:
{message}

Rules:
- Safety concerns → High Priority
- Infrastructure → Maintenance
- Social support → Community Team
- Keep response concise
"""

    try:

        response = client.chat.completions.create(
            model="gpt-5-mini",

            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception:

        return """
Category: General
Priority: Medium
Assigned Team: Community Team
Suggested Action:
Manual review required
"""


# -----------------------------------
# PARSER
# -----------------------------------

def extract_field(text, field):

    try:

        for line in text.splitlines():

            if line.lower().startswith(
                field.lower()
            ):

                return (
                    line
                    .split(":", 1)[1]
                    .strip()
                )

    except:
        pass

    return "Unknown"


# -----------------------------------
# REQUEST ID
# -----------------------------------

def generate_request_id(issue_id):

    return f"CS-{str(issue_id).zfill(3)}"


# -----------------------------------
# WHATSAPP WEBHOOK
# -----------------------------------

@app.post("/whatsapp")

async def whatsapp_reply(
    request: Request
):

    try:

        form = await request.form()

        incoming_msg = (
            form.get("Body", "")
            .strip()
        )

        if not incoming_msg:

            xml = """
<Response>
<Message>
Please send a valid request.
</Message>
</Response>
"""

            return Response(
                content=xml,
                media_type="application/xml"
            )

        # -----------------
        # AI
        # -----------------

        ai_result = classify_issue(
            incoming_msg
        )

        category = extract_field(
            ai_result,
            "Category"
        )

        priority = extract_field(
            ai_result,
            "Priority"
        )

        assigned_team = extract_field(
            ai_result,
            "Assigned Team"
        )

        action = extract_field(
            ai_result,
            "Suggested Action"
        )

        # -----------------
        # SAVE
        # -----------------

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

        db.refresh(issue)

        request_id = generate_request_id(
            issue.id
        )

        db.close()

        # -----------------
        # RESPONSE
        # -----------------

        reply = f"""
CommuniSync AI

Request ID: {request_id}

Category: {category}

Priority: {priority}

Assigned Team: {assigned_team}

Suggested Action:
{action}

Your request has been routed successfully.
"""

        xml = f"""
<Response>
<Message>
{reply}
</Message>
</Response>
"""

        return Response(
            content=xml,
            media_type="application/xml"
        )

    except Exception:

        xml = """
<Response>
<Message>
CommuniSync AI

Something went wrong.
Please try again.
</Message>
</Response>
"""

        return Response(
            content=xml,
            media_type="application/xml"
        )


# -----------------------------------
# HEALTH CHECK
# -----------------------------------

@app.get("/")

def home():

    return {
        "status": "running",
        "service": "CommuniSync AI"
    }