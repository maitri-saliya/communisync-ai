from sqlalchemy import *
from sqlalchemy.orm import *

engine=create_engine(
    "sqlite:///communi.db",
    connect_args={"check_same_thread":False}
)

Base=declarative_base()

class Need(Base):
    __tablename__="needs"

    id=Column(Integer,primary_key=True)

    user=Column(String)

    category=Column(String)

    type=Column(String)

    urgency=Column(Integer)

    description=Column(String)

Session=sessionmaker(bind=engine)

Base.metadata.create_all(engine)