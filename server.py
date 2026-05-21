from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import Response

from database import SessionLocal
from models import Issue

from twilio.rest import Client

from openai import OpenAI

from teams import TEAM_NUMBERS

import os


app = FastAPI()


client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


twilio = Client(

    os.getenv(
        "TWILIO_ACCOUNT_SID"
    ),

    os.getenv(
        "TWILIO_AUTH_TOKEN"
    )
)


def classify_issue(message):

    prompt = f"""
Analyze request.

Return ONLY:

Category:
Priority:
Assigned Team:
Suggested Action:

Request:
{message}
"""

    result = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "system",

                "content":
                prompt
            }
        ]
    )

    return (
        result
        .choices[0]
        .message
        .content
    )


def extract(text, field):

    for line in text.splitlines():

        if line.lower().startswith(
            field.lower()
        ):

            return (
                line
                .split(":", 1)[1]
                .strip()
            )

    return "Unknown"


def notify_team(

    request_id,

    team,

    issue,

    priority,

    action
):

    phone = TEAM_NUMBERS.get(
        team
    )

    if not phone:
        return

    text = f"""
🚨 CommuniSync Alert

Request:
{request_id}

Issue:
{issue}

Priority:
{priority}

Suggested Action:
{action}
"""

    twilio.messages.create(

        from_=os.getenv(
            "TWILIO_WHATSAPP_NUMBER"
        ),

        to=phone,

        body=text
    )


@app.post(
    "/whatsapp"
)

async def whatsapp(
    request: Request
):

    form = await request.form()

    message = (
        form
        .get(
            "Body",
            ""
        )
    )

    result = (
        classify_issue(
            message
        )
    )

    category = extract(
        result,
        "Category"
    )

    priority = extract(
        result,
        "Priority"
    )

    team = extract(
        result,
        "Assigned Team"
    )

    action = extract(
        result,
        "Suggested Action"
    )

    db = SessionLocal()

    issue = Issue(

        message=message,

        category=category,

        priority=priority,

        assigned_team=team,

        suggested_action=action,

        status="Pending"
    )

    db.add(
        issue
    )

    db.commit()

    db.refresh(
        issue
    )

    request_id = (
        f"CS-{issue.id}"
    )

    notify_team(

        request_id,

        team,

        message,

        priority,

        action
    )

    db.close()

    reply = f"""
CommuniSync AI

Request:
{request_id}

Category:
{category}

Priority:
{priority}

Assigned Team:
{team}

Suggested:
{action}

Request routed.
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

        media_type=
        "application/xml"
    )