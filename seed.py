from database import *

session=Session()

demo_data=[

Need(
user="Elderly Couple",
contact="whatsapp:+919845401200",
category="food",
type="need",
urgency=5,
description="Need dinner"
),

Need(
user="Volunteer",
contact="whatsapp:+918082094901",
category="transport",
type="offer",
urgency=2,
description="Can deliver"
),

Need(
user="Student",
contact="whatsapp:+918555870631",
category="repair",
type="need",
urgency=3,
description="Need appliance repair"
),

Need(
user="Neighbour",
contact="whatsapp:+918369366339",
category="food",
type="offer",
urgency=1,
description="Extra meals"
)

]

session.add_all(demo_data)

session.commit()

print("Seeded")