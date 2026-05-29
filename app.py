from fastapi import FastAPI, Form
from fastapi.responses import Response

from twilio.twiml.messaging_response import MessagingResponse

from database import SessionLocal
from models import RequestLog

from ai_service import understand
from matcher import route_request


# ----------------------------------
# APP
# ----------------------------------

app = FastAPI()


@app.get("/")
def health():

    return {
        "status": "CommuniSync running"
    }


# ----------------------------------
# WHATSAPP WEBHOOK
# ----------------------------------

@app.post("/webhook")
async def webhook(

    Body: str = Form(...),

    From: str = Form(...)
):

    db = SessionLocal()

    try:

        # ----------------------------------
        # AI UNDERSTANDING
        # ----------------------------------

        result = understand(Body)

        print(result)

        # ----------------------------------
        # EXTRACT
        # ----------------------------------

        request_type = result.get(
            "type",
            "need"
        )

        category = result.get(
            "category",
            "general"
        )

        urgency = result.get(
            "urgency",
            3
        )

        priority = result.get(
            "priority",
            "Medium"
        )

        team = result.get(
            "team",
            "Community Team"
        )

        action = result.get(
            "suggested_action",
            "Manual review"
        )

        description = result.get(
            "short_description",
            Body
        )

        # ----------------------------------
        # SAVE TO DB
        # ----------------------------------

        row = RequestLog(

            requester=From,

            category=category,

            request_type=request_type,

            urgency=urgency,

            priority=priority,

            assigned_team=team,

            suggested_action=action,

            description=description,

            status="Pending"
        )

        db.add(row)

        db.commit()

        db.refresh(row)

        # ----------------------------------
        # ROUTE REQUEST
        # ----------------------------------

        route_request(

            requester=From,

            category=category,

            urgency=urgency,

            team=team,

            description=description
        )

        # ----------------------------------
        # USER REPLY
        # ----------------------------------

        response = MessagingResponse()

        response.message(
f"""
🤝 CommuniSync AI

Request ID:
CS-{row.id}

Category:
{category}

Priority:
{priority}

Assigned Team:
{team}

Suggested Action:
{action}

Your request has been routed.
"""
        )

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    except Exception as e:

        print("ERROR:", e)

        response = MessagingResponse()

        response.message(
"""
CommuniSync AI

We received your request.

Support team has been notified.
"""
        )

        return Response(
            content=str(response),
            media_type="application/xml"
        )

    finally:

        db.close()
