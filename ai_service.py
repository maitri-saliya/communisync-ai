import os
import json

from openai import AzureOpenAI


# ----------------------------------
# AZURE CLIENT
# ----------------------------------

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


# ----------------------------------
# DEFAULTS
# ----------------------------------

DEFAULT_RESULT = {

    "type":
    "need",

    "category":
    "general",

    "urgency":
    3,

    "priority":
    "Medium",

    "short_description":
    "General issue",

    "team":
    "Community Team",

    "suggested_action":
    "Manual review"
}


# ----------------------------------
# AI UNDERSTANDING
# ----------------------------------


def understand(text):

    try:

        response = (
            client.chat.completions.create(

                model=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),

                response_format={
                    "type": "json_object"
                },

                temperature=0,

                messages=[

                    {
                        "role": "system",

                        "content": """
You are CommuniSync AI.

Classify community requests.

Return ONLY valid JSON.

{
    "type":"need|offer",
    "category":"single lowercase word",
    "urgency":1-5,
    "priority":"Low|Medium|High",
    "short_description":"brief summary",
    "team":"Utility Team|Civic Team|Community Team|Repair Team|Transport Team",
    "suggested_action":"short action"
}

Rules:

- Streetlight / roads -> Civic Team
- Water / electricity / garbage -> Utility Team
- Appliance / equipment repair -> Repair Team
- Delivery / transport -> Transport Team
- Food / health / events -> Community Team
- Unknown -> Community Team

Urgency:
5 = emergency
4 = severe
3 = normal
2 = minor
1 = suggestion

Priority:
1-2 = Low
3 = Medium
4-5 = High

No explanation.
"""
                    },

                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        result = json.loads(content)

        for key, value in DEFAULT_RESULT.items():

            if (
                key not in result
                or result[key] in [None, ""]
            ):

                result[key] = value

        return result

    except Exception as e:

        print("Azure Error:", str(e))

        return DEFAULT_RESULT
