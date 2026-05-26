import os
import json
from openai import AzureOpenAI


CATEGORIES = {
    "food": [
        "food",
        "meal",
        "hungry",
        "dinner",
        "lunch"
    ],
    "repair": [
        "repair",
        "electrician",
        "fix",
        "appliance"
    ],
    "transport": [
        "transport",
        "delivery",
        "ride",
        "groceries"
    ],
    "community": [
        "volunteer",
        "help",
        "support"
    ]
}


def detect_category(text):

    text = text.lower()

    for category, words in CATEGORIES.items():

        if any(
            word in text
            for word in words
        ):
            return category

    return "community"


def understand(text):

    try:

        client = AzureOpenAI(
            api_key=os.getenv(
                "AZURE_OPENAI_KEY"
            ),
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv(
                "AZURE_OPENAI_ENDPOINT"
            )
        )

        response = (
            client.chat.completions.create(
                model=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),
                messages=[
                    {
                        "role":"system",
                        "content":"""
Return JSON:

{
"type":"",
"category":"",
"urgency":1,
"short_description":""
}
"""
                    },
                    {
                        "role":"user",
                        "content":text
                    }
                ],

                response_format={
                    "type":"json_object"
                }
            )
        )

        return json.loads(
            response
            .choices[0]
            .message.content
        )

    except Exception:

        return {
            "type":
            (
                "offer"
                if "have" in text.lower()
                else "need"
            ),

            "category":
            detect_category(text),

            "urgency":3,

            "short_description":
            text
        }