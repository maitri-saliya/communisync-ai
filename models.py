from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Issue(Base):

    __tablename__ = "issues"

    id = Column(
        Integer,
        primary_key=True
    )

    message = Column(String)

    category = Column(String)

    priority = Column(String)

    assigned_team = Column(String)

    suggested_action = Column(String)

    status = Column(String)