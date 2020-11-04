"""
Create a Sailors and Boats dataset in Python
Modified from @eugsokolov
"""
from collections import namedtuple
import datetime

from . import Base
from .sailors import Sailor
from .reserves import Reserve
from .boats import Boat

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sailors = [
    (22, "dusting", 7, 45.0),
    (23, "emilio", 7, 45.0),
    (24, "scruntus", 1, 33.0),
    (29, "brutus", 1, 33.0),
    (31, "lubber", 8, 55.5),
    (32, "andy", 8, 25.5),
    (35, "figaro", 8, 55.5),
    (58, "rusty", 10, 35),
    (59, "stum", 8, 25.5),
    (60, "jit", 10, 35),
    (61, "ossola", 7, 16),
    (62, "shaun", 10, 35),
    (64, "horatio", 7, 16),
    (71, "zorba", 10, 35),
    (74, "horatio", 9, 25.5),
    (85, "art", 3, 25.5),
    (88, "kevin", 3, 25.5),
    (89, "will", 3, 25.5),
    (90, "josh", 3, 25.5),
    (95, "bob", 3, 63.5),
]

boats = [
    (101, "Interlake", "blue", 45, 1),
    (102, "Interlake", "red", 45, 2),
    (103, "Clipper", "green", 40, 1),
    (104, "Clipper", "red", 40, 1),
    (105, "Marine", "red", 35, 2),
    (106, "Marine", "green", 35, 1),
    (107, "Marine", "blue", 35, 1),
    (108, "Driftwood", "red", 35, 2),
    (109, "Driftwood", "blue", 35, 2),
    (110, "Klapser", "red", 30, 2),
    (111, "Sooney", "green", 28, 2),
    (112, "Sooney", "red", 28, 2),
]

reserves = [
    (22, 101, "1998-10-10", 3, 5),
    (22, 102, "1998-10-10", 2, 4),
    (22, 103, "1998-08-10", 1, 3),
    (22, 104, "1998-07-10", 5, 5),
    (23, 104, "1998-10-10", 6, 2),
    (23, 105, "1998-11-10", 2, 3),
    (24, 104, "1998-10-10", 2, 4),
    (31, 102, "1998-11-10", 1, 5),
    (31, 103, "1998-11-06", 5, 4),
    (31, 104, "1998-11-12", 6, 2),
    (35, 104, "1998-08-10", 10, 4),
    (35, 105, "1998-11-06", 1, 1),
    (59, 105, "1998-07-10", 2, 5),
    (59, 106, "1998-11-12", 3, 4),
    (59, 109, "1998-11-10", 4, 2),
    (60, 106, "1998-09-05", 5, 3),
    (60, 106, "1998-09-08", 1, 5),
    (60, 109, "1998-07-10", 2, 5),
    (61, 112, "1998-09-08", 1, 1),
    (62, 110, "1998-11-06", 5, 1),
    (64, 101, "1998-09-05", 1, 1),
    (64, 102, "1998-09-08", 2, 2),
    (74, 103, "1998-09-08", 1, 5),
    (88, 107, "1998-09-08", 5, 5),
    (88, 110, "1998-09-05", 2, 5),
    (88, 110, "1998-11-12", 1, 4),
    (88, 111, "1998-09-08", 5, 4),
    (89, 108, "1998-10-10", 2, 3),
    (89, 109, "1998-08-10", 1, 5),
    (90, 109, "1998-10-10", 1, 3),
]

S = namedtuple("S", ["sid", "sname", "rating", "age"])
B = namedtuple("B", ["bid", "bname", "color", "length", "location"])
R = namedtuple("R", ["sid", "bid", "day", "price", "rating"])

sailors = list(map(lambda x: Sailor(**S(*x)._asdict()), sailors))
boats = list(map(lambda x: Boat(**B(*x)._asdict()), boats))
reserves = list(map(lambda x: Reserve(**R(*x)._asdict()), reserves))
