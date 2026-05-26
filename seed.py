from database import Session, Need

s = Session()

s.query(Need).delete()

demo = [

Need(
user="Food Volunteer",
contact="whatsapp:+918369366339",
category="food",
type="offer",
urgency=1,
description="Meals available"
),

Need(
user="Repair Volunteer",
contact="whatsapp:+918555870631",
category="repair",
type="offer",
urgency=1,
description="Repair support"
),

Need(
user="Transport Volunteer",
contact="whatsapp:+917411395906",
category="transport",
type="offer",
urgency=1,
description="Delivery help"
),

Need(
user="Community Team",
contact="whatsapp:+919845401200",
category="general",
type="offer",
urgency=1,
description="General support"
)

]

s.add_all(demo)

s.commit()

print("Demo data inserted")