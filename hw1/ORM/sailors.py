from . import Base
from sqlalchemy import Column, Integer, String, Float


class Sailor(Base):
    __tablename__ = "sailors"

    sid = Column(Integer, primary_key=True)
    sname = Column(String(30))
    rating = Column(Integer)
    age = Column(Float)
        
    def __repr__(self):
        return f"<Sailor(id={self.sid}, name={self.sname}, rating={self.rating}, age={self.age})>"
