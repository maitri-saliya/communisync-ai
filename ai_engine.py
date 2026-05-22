import requests


def classify_issue(message):

    prompt = f"""
Analyze community request.

Return ONLY:

Category:
Priority:
Assigned Team:
Suggested Action:

Request:
{message}

Rules:

- Streetlight → Maintenance Team
- Roads → Maintenance Team
- Water / Pool / Garbage → Utility Team
- Broken equipment → Repair Team
- Events / Food / Health → Community Team
"""

    try:

        response = requests.post(

            "http://localhost:11434/api/generate",

            json={

                "model":
                "mistral",

                "prompt":
                prompt,

                "stream":
                False
            },

            timeout=60
        )

        return (
            response
            .json()["response"]
        )

    except:

        return """
Category: General
Priority: Medium
Assigned Team: Community Team
Suggested Action: Manual review
"""