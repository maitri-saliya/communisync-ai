from fastapi import FastAPI, Form
from twilio.twiml.messaging_response import MessagingResponse

from database import *
from ai_service import *
from matcher import *

app=FastAPI()

@app.post("/webhook")
async def webhook(
    Body:str=Form(...)
):

    result=understand(Body)

    session=Session()

    row=Need(
        user="demo",
        category=result["category"],
        type=result["type"],
        urgency=result["urgency"],
        description=result["short_description"]
    )

    session.add(row)

    session.commit()

    matched,msg=find_match(result)

    tw=MessagingResponse()

    tw.message(
f"""
CommuniSync AI

Type:
{result["type"]}

Category:
{result["category"]}

Urgency:
{result["urgency"]}

{msg}
"""
)

    return str(tw)