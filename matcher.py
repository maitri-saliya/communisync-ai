from teams import TEAM_NUMBERS
from notification_service import send_assignment


DEFAULT_TEAM = (
    TEAM_NUMBERS[
        "Community Team"
    ]
)


# ----------------------------------
# ROUTE REQUEST
# ----------------------------------


def route_request(

    requester,

    category,

    urgency,

    team,

    description
):

    assigned_number = (

        TEAM_NUMBERS.get(team)

        or DEFAULT_TEAM

    )

    send_assignment(

        to_number=assigned_number,

        requester=requester,

        category=category,

        description=description,

        urgency=urgency,

        assigned_team=team
    )

    print(
        f"Forwarded to {team}"
    )
