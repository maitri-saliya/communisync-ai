from database import Session, Need
from teams import TEAM_NUMBERS
from notification_service import send_assignment


DEFAULT_TEAM = TEAM_NUMBERS["general"]


def find_match(data):

    session = Session()

    category = (
        data.get("category")
        or "general"
    ).lower()

    request_type = (
        data.get("type")
        or "need"
    ).lower()

    requester = data.get(
        "requester",
        "Anonymous"
    )

    opposite = (
        "offer"
        if request_type == "need"
        else "need"
    )

    records = (
        session.query(Need)
        .filter(
            Need.category.ilike(
                category
            ),

            Need.type.ilike(
                opposite
            ),

            Need.contact != requester
        )
        .all()
    )

    if records:

        match = records[0]

        send_assignment(
            to_number=match.contact,
            requester=requester,
            category=category,
            description=data[
                "short_description"
            ],
            urgency=data["urgency"],
            is_match=True
        )

        return (
            True,
            f"""
Matched successfully.

Assigned:
{match.user}

Contact:
{match.contact}
"""
        )

    redirected = TEAM_NUMBERS.get(
        category,
        DEFAULT_TEAM
    )

    send_assignment(
        to_number=redirected,
        requester=requester,
        category=category,
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

Forwarded to:
{redirected}
"""
    )