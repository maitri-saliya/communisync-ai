from database import *
from teams import TEAM_NUMBERS


DEFAULT_TEAM = TEAM_NUMBERS["general"]


def find_match(data):

    session = Session()

    opposite = (
        "offer"
        if data["type"] == "need"
        else "need"
    )

    match = (
        session.query(Need)
        .filter(
            Need.category == data["category"],
            Need.type == opposite
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

    redirected_team = TEAM_NUMBERS.get(
        data["category"],
        DEFAULT_TEAM
    )

    return (
        False,
        f"""
No direct match.

Your request has been routed to Community Support.

Contact:
{redirected_team}
"""
    )