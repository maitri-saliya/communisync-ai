import json
from openai import AzureOpenAI
import os

client=AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-08-01-preview",
    azure_endpoint=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )
)

DEPLOYMENT=os.getenv(
    "AZURE_OPENAI_DEPLOYMENT"
)

def understand(text):

    prompt=f"""
Return JSON only.

Input:
{text}

Extract:
- type (need/offer)
- category
- urgency (1-5)
- short_description
"""

    r=client.chat.completions.create(
        model=DEPLOYMENT,
        messages=[
            {"role":"system","content":
             "Community matching AI"},
            {"role":"user","content":prompt}
        ]
    )

    return json.loads(
        r.choices[0].message.content
    )