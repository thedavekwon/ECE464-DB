from . import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import backref, relationship

class Boat(Base):
    __tablename__ = "boats"
    
    bid = Column(Integer, primary_key=True)
    bname = Column(String(20))
    color = Column(String(10))
    length = Column(Integer)
    
    reservations = relationship('Reserve',
                                backref=backref('boat', cascade='delete'))
    
    def __init__(self, bid, bname, color, length):
        self.bid = bid
        self.bname = bname
        self.color = color
        self.length = length
    
    def __repr__(self):
        return f"<Boat(id={self.bid}, name={self.bname}, color={self.color}, length={self.length})>"