from database import *
from teams import TEAM_NUMBERS


def find_match(data):

    session=Session()

    opposite=(
        "offer"
        if data["type"]=="need"
        else "need"
    )

    match=(
        session.query(Need)
        .filter(
            Need.category==
            data["category"],

            Need.type==
            opposite
        )
        .first()
    )

    if match:

        return (
            True,
            f"""
Matched!

Resource:
{match.user}

Contact:
{match.contact}

Approx distance:
1.5 km
"""
        )

    fallback=TEAM_NUMBERS.get(
        data["category"]
    )

    return (
        False,
        f"""
No direct match.

Forwarded to:
{fallback}
"""
    )