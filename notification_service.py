import os
from twilio.rest import Client


client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

FROM_NUMBER = os.getenv(
    "TWILIO_WHATSAPP_NUMBER"
)


def send_assignment(
    to_number,
    requester,
    category,
    description,
    urgency,
    is_match=True
):

    status = (
        "✅ MATCH FOUND"
        if is_match
        else "🚨 NEW REQUEST"
    )

    body = f"""
{status}

CommuniSync AI

Requester:
{requester}

Category:
{category}

Urgency:
{urgency}/5

Requirement:
{description}

Please respond if available.
"""

    try:

        client.messages.create(
            body=body,
            from_=FROM_NUMBER,
            to=to_number
        )

    except Exception as e:
        print(e)