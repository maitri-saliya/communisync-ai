from database import *
from teams import TEAM_NUMBERS
from notification_service import (
    send_assignment
)

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
            Need.category ==
            data["category"],

            Need.type ==
            opposite
        )
        .first()
    )

    if match:

        send_assignment(
            to_number=match.contact,
            requester=data["requester"],
            category=data["category"],
            description=data[
                "short_description"
            ],
            urgency=data["urgency"],
            is_match=True
        )

        return (
            True,
            f"""
Matched!

Request forwarded.

Contact:
{match.contact}

Distance:
1.5 km
"""
        )

    redirected = TEAM_NUMBERS.get(
        data["category"],
        DEFAULT_TEAM
    )

    send_assignment(
        to_number=redirected,
        requester=data["requester"],
        category=data["category"],
        description=data[
            "short_description"
        ],
        urgency=data["urgency"],
        is_match=False
    )

    return (
        False,
        f"""
No direct match.

Forwarded to support.

Contact:
{redirected}
"""
    )