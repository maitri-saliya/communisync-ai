from fastapi import FastAPI, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

from database import Session, Need
from ai_service import understand
from matcher import find_match

app = FastAPI()


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/webhook")
async def webhook(
    Body: str = Form(...)
):

    result = understand(Body)

    session = Session()

    row = Need(
        user="demo",
        category=result["category"],
        type=result["type"],
        urgency=result["urgency"],
        description=result["short_description"]
    )

    session.add(row)
    session.commit()

    matched, msg = find_match(result)

    response = MessagingResponse()

    response.message(
        f"""
CommuniSync AI

Type: {result["type"]}
Category: {result["category"]}
Urgency: {result["urgency"]}

{msg}
"""
    )

    return Response(
        content=str(response),
        media_type="application/xml"
    )