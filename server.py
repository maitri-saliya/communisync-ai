from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()


def classify_issue(message):

    msg = message.lower()

    if "water" in msg:
        return (
            "Category: Emergency\n"
            "Priority: High\n"
            "Assigned Team: Utility Team"
        )

    elif "light" in msg:
        return (
            "Category: Maintenance\n"
            "Priority: Medium\n"
            "Assigned Team: Civic Team"
        )

    return (
        "Category: General\n"
        "Priority: Low\n"
        "Assigned Team: Community Team"
    )


app = FastAPI()


@app.post("/whatsapp")
async def whatsapp_reply(request: Request):

    form = await request.form()

    message = form.get("Body", "")

    result = classify_issue(message)

    xml = f"""
<Response>
<Message>
CommuniSync AI

{result}

Request routed successfully.
</Message>
</Response>
"""

    return Response(
        content=xml,
        media_type="application/xml"
    )