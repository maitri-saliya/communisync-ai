from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from database import Session, Need
from ai_service import understand
from matcher import find_match

app = FastAPI()


@app.get("/")
def health():

    return {
        "status": "CommuniSync running"
    }


@app.post("/webhook")
async def webhook(

    Body: str = Form(...),

    From: str = Form(...)

):

    try:

        # --------------------
        # AI Extraction
        # --------------------

        result = understand(Body)

        result["requester"] = From

        category = result.get(
            "category",
            "general"
        )

        request_type = result.get(
            "type",
            "need"
        )

        urgency = result.get(
            "urgency",
            3
        )

        description = result.get(
            "short_description",
            Body
        )

        # --------------------
        # Save request
        # --------------------

        session = Session()

        row = Need(

            user=From,

            contact=From,

            category=category,

            type=request_type,

            urgency=urgency,

            description=description
        )

        session.add(row)

        session.commit()

        # --------------------
        # Match + Notify
        # --------------------

        matched, message = find_match(
            {
                "requester": From,

                "type": request_type,

                "category": category,

                "urgency": urgency,

                "short_description":
                description
            }
        )

        # --------------------
        # WhatsApp Reply
        # --------------------

        response = MessagingResponse()

        response.message(
f"""
🤝 CommuniSync AI

Request received.

Type:
{request_type}

Category:
{category}

Urgency:
{urgency}/5

Details:
{description}

{message}
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