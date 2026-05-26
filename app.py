from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from database import Session, Need
from ai_service import understand
from matcher import find_match

from dashboard import router as dashboard_router

app = FastAPI()

app.include_router(
    dashboard_router
)

@app.on_event(
"startup"
)

def seed():

    session=Session()

    if (
        session
        .query(Need)
        .count()
        ==0
    ):

        session.add_all([

Need(
user="Food Volunteer",

contact=
"whatsapp:+918369366339",

category="food",

type="offer",

urgency=1,

description=
"Meals available"
),

Need(
user="Community Team",

contact=
"whatsapp:+919845401200",

category="general",

type="offer",

urgency=1,

description=
"General support"
)

])

        session.commit()

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
                "requester":
                From,

                "type":
                request_type,

                "category":
                category,

                "urgency":
                urgency,

                "team":
                result.get(
                "team"
                ),

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