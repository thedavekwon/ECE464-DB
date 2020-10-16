import datetime

from . import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import backref, relationship


class Reserve(Base):
    __tablename__ = "reserves"
    __table_args__ = (PrimaryKeyConstraint("sid", "bid", "day"), {})

    sid = Column(Integer, ForeignKey("sailors.sid"))
    bid = Column(Integer, ForeignKey("boats.bid"))
    day = Column(DateTime)
    price = Column(Integer, default=0)

    sailor = relationship("Sailor")

    def __init__(self, sid, bid, day, price):
        self.sid = sid
        self.bid = bid
        self.day = datetime.datetime.strptime(day, "%Y-%m-%d")
        self.price = price

    def __repr__(self):
        return f"<Reservation(sid={self.sid}, bid={self.bid}, day={self.day}, price={self.price})>"
