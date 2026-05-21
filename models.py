from sqlalchemy import Column, Integer, String

from database import Base


class Issue(Base):

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)

    message = Column(String)

    category = Column(String)

    priority = Column(String)

    assigned_team = Column(String)

    status = Column(String)