import os

from twilio.rest import Client


# ----------------------------------
# TWILIO
# ----------------------------------

client = Client(

    os.getenv(
        "TWILIO_ACCOUNT_SID"
    ),

    os.getenv(
        "TWILIO_AUTH_TOKEN"
    )
)


# ----------------------------------
# SEND ASSIGNMENT
# ----------------------------------


def send_assignment(

    to_number,

    requester,

    category,

    description,

    urgency,

    assigned_team
):

    try:

        client.messages.create(

            from_=os.getenv(
                "TWILIO_WHATSAPP_NUMBER"
            ),

            to=to_number,

            body=f"""
🚨 CommuniSync Alert

Requester:
{requester}

Category:
{category}

Urgency:
{urgency}/5

Assigned Team:
{assigned_team}

Issue:
{description}
"""
        )

        print(
            f"Notification sent to {to_number}"
        )

    except Exception as e:

        print(
            "Twilio Error:",
            str(e)
        )
