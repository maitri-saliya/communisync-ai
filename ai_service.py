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
    "",

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
                    "type":
                    "json_object"
                },

                temperature=0,

                messages=[

                    {
                        "role":
                        "system",

                        "content":
"""
You are CommuniSync AI.

You classify community issues and requests.

Return ONLY valid JSON.

Schema:

{
    "type":"need|offer",

    "category":"single lowercase word",

    "urgency":1-5,

    "priority":"Low|Medium|High",

    "short_description":"brief summary",

    "team":"Utility Team|Civic Team|Community Team|Repair Team|Maintenance Team|Neighbor",

    "suggested_action":"short action"
}

Classification Rules:

- Streetlight problems -> Civic Team
- Roads / potholes -> Civic Team
- Garbage / drainage / sewage -> Utility Team
- Water supply -> Utility Team
- Electricity -> Utility Team
- Broken equipment -> Maintenance Team
- Appliance repair -> Repair Team
- Borrow / help / assistance -> Neighbor
- Food / health / donation -> Community Team
- Community event -> Community Team

Urgency Rules:

5 = emergency / danger / medical
4 = severe disruption
3 = standard issue
2 = minor issue
1 = suggestion / low importance

Priority Mapping:

urgency 1-2 -> Low
urgency 3 -> Medium
urgency 4-5 -> High

Rules:

- Always assign exactly one team.
- Never return null.
- Keep category short.
- Use lowercase category.
- Keep suggested_action under 10 words.
- If uncertain use:
  team = Community Team
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

        content = (
            response
            .choices[0]
            .message
            .content
        )

        result = json.loads(
            content
        )

        # ----------------------------------
        # SAFETY FALLBACKS
        # ----------------------------------

        for key, value in DEFAULT_RESULT.items():

            if (

                key not in result
                or result[key] in [None, ""]

            ):

                result[key] = value

        # Ensure urgency valid

        if not isinstance(
            result["urgency"],
            int
        ):

            result["urgency"] = 3

        result["urgency"] = max(
            1,
            min(
                5,
                result["urgency"]
            )
        )

        return result

    except Exception as e:

        print(
            "Azure AI Error:",
            str(e)
        )

        fallback = DEFAULT_RESULT.copy()

        fallback[
            "short_description"
        ] = text

        return fallback