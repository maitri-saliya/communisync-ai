from database import *

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
            Need.category==data["category"],
            Need.type==opposite
        )
        .first()
    )

    if match:
        return (
            True,
            f"Matched nearby resource."
        )

    return (
        False,
        "No match yet. Added to queue."
    )