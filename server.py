from fastapi import FastAPI, Request
from fastapi.responses import Response

from database import SessionLocal
from models import Issue

from twilio.rest import Client

from openai import AzureOpenAI

from teams import TEAM_NUMBERS

import os


# ----------------------------------
# APP
# ----------------------------------

app = FastAPI()


# ----------------------------------
# AZURE OPENAI
# ----------------------------------

client = AzureOpenAI(

    api_key=os.getenv(
        "AZURE_OPENAI_API_KEY"
    ),

    api_version="2024-10-21",

    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )
)


# ----------------------------------
# TWILIO
# ----------------------------------

twilio = Client(

    os.getenv(
        "TWILIO_ACCOUNT_SID"
    ),

    os.getenv(
        "TWILIO_AUTH_TOKEN"
    )
)


# ----------------------------------
# AI CLASSIFICATION
# ----------------------------------

def classify_issue(message):

    try:

        result = (
            client
            .chat
            .completions
            .create(

                model=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),

                messages=[

                    {
                        "role": "system",

                        "content": """
You are CommuniSync AI.

Analyze community requests.

Return EXACTLY:

Category: <value>
Priority: <Low/Medium/High>
Assigned Team: <value>
Suggested Action: <value>

No explanation.
"""
                    },

                    {
                        "role": "user",

                        "content": message
                    }

                ],

                temperature=0
            )
        )

        content = (
            result
            .choices[0]
            .message
            .content
        )

        if not content:

            return """
Category: Unknown
Priority: Medium
Assigned Team: General
Suggested Action: Manual review
"""

        return content

    except Exception as e:

        print(
            f"Azure Error: {e}"
        )

        return """
Category: Unknown
Priority: Medium
Assigned Team: General
Suggested Action: Manual review
"""


# ----------------------------------
# PARSE RESPONSE
# ----------------------------------

def extract(
    text,
    field
):

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


# ----------------------------------
# SEND WHATSAPP ALERT
# ----------------------------------

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

        print(
            f"No number configured for {team}"
        )

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

    try:

        twilio.messages.create(

            from_=os.getenv(
                "TWILIO_WHATSAPP_NUMBER"
            ),

            to=phone,

            body=text
        )

    except Exception as e:

        print(
            f"Twilio Error: {e}"
        )


# ----------------------------------
# WHATSAPP WEBHOOK
# ----------------------------------

@app.post(
    "/whatsapp"
)

async def whatsapp(

    request: Request

):

    db = None

    try:

        form = (
            await request.form()
        )

        message = (

            form.get(
                "Body",
                ""
            )
            .strip()

        )

        if not message:

            return Response(

                content="""
<Response>
<Message>
Please send a request.
</Message>
</Response>
""",

                media_type="application/xml"
            )

        result = (
            classify_issue(
                message
            )
        )

        category = (
            extract(
                result,
                "Category"
            )
        )

        priority = (
            extract(
                result,
                "Priority"
            )
        )

        team = (
            extract(
                result,
                "Assigned Team"
            )
        )

        action = (
            extract(
                result,
                "Suggested Action"
            )
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

Request routed successfully.
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

    except Exception as e:

        print(
            f"Webhook Error: {e}"
        )

        return Response(

            content="""
<Response>
<Message>
Something went wrong.
Please try again.
</Message>
</Response>
""",

            media_type="application/xml"
        )

    finally:

        if db:

            db.close()

print(
    os.getenv(
        "DATABASE_URL"
    )
)