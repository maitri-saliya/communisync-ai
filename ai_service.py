import os
import json
from openai import AzureOpenAI


client = AzureOpenAI(
    api_key=os.getenv(
        "AZURE_OPENAI_KEY"
    ),
    api_version=
    "2024-08-01-preview",
    azure_endpoint=
    os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )
)


TEAM_MAP = {

    "utility":
    "Utility Team",

    "civic":
    "Civic Team",

    "community":
    "Community Team",

    "repair":
    "Repair Team"
}


def understand(text):

    try:

        response = (
            client.chat.completions.create(

                model=
                os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),

                response_format={
                    "type":
                    "json_object"
                },

                messages=[

                    {
                        "role":
                        "system",

                        "content":
"""
You are CommuniSync AI.

Extract JSON only.

{
"type":"need|offer",

"category":"single word",

"urgency":1-5,

"short_description":"",

"team":"Utility Team | Civic Team | Community Team | Repair Team"
}

Rules:

food → Community Team

repair →
Repair Team

electricity →
Utility Team

road/public →
Civic Team

unknown →
Community Team
"""
                    },

                    {
                        "role":
                        "user",

                        "content":
                        text
                    }
                ]
            )
        )

        result = json.loads(
            response
            .choices[0]
            .message
            .content
        )

        if (
            not result.get(
                "team"
            )
        ):
            result[
                "team"
            ] = (
                "Community Team"
            )

        return result

    except Exception as e:

        print(e)

        return {

            "type":
            "need",

            "category":
            "general",

            "urgency":
            3,

            "short_description":
            text,

            "team":
            "Community Team"
        }