import os
import json
from openai import AzureOpenAI


def understand(text):

    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-08-01-preview",
        azure_endpoint=os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        )
    )

    deployment = os.getenv(
        "AZURE_OPENAI_DEPLOYMENT"
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "Extract structured data"
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    try:
        return json.loads(
            response.choices[0]
            .message.content
        )

    except:
        return {
            "type": "need",
            "category": "general",
            "urgency": 3,
            "short_description": text
        }