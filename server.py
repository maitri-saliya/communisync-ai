from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()


@app.post("/whatsapp")
async def whatsapp_reply(request: Request):

    xml = """
<Response>
<Message>
Hello from CommuniSync 🚀
</Message>
</Response>
"""

    return Response(
        content=xml,
        media_type="application/xml"
    )