from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database import Base
from database import engine


class RequestLog(Base):

    __tablename__ = "requests"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    requester = Column(
        String
    )

    category = Column(
        String
    )

    request_type = Column(
        String
    )

    urgency = Column(
        Integer
    )

    priority = Column(
        String
    )

    assigned_team = Column(
        String
    )

    suggested_action = Column(
        String
    )

    description = Column(
        String
    )

    status = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


Base.metadata.create_all(
    bind=engine
)
