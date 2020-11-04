import datetime
import pytest

from ORM import Base
from ORM.sailors import Sailor
from ORM.reserves import Reserve
from ORM.boats import Boat
from ORM.test_data import sailors, boats, reserves

from sqlalchemy import create_engine, func, desc, case, asc
from sqlalchemy.sql import label, and_, text
from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased

# Use session since we only have query to DB for testing
@pytest.fixture(scope="session")
def engine():
    # create in-memory sqlite db for testing
    engine = create_engine("sqlite:///:memory:", echo=False)
    # Create tables from models
    Base.metadata.create_all(engine)

    yield engine

    # Remove in-memory engine
    engine.dispose()


@pytest.fixture(scope="session")
def session(engine):
    # Create a session to insert rows
    session = Session(bind=engine)
    # Add test data
    session.add_all(sailors + boats + reserves)

    yield session

    session.rollback()
    session.close()


# List, for every boat, the number of times it has been reserved,
# excluding those boats that have never been reserved (list the id and the name).
def test_1(engine, session):
    squery = (
        session.query(Reserve.bid, label("reserve_count", func.count()))
        .group_by(Reserve.bid)
        .subquery()
    )
    query = (
        session.query(Boat.bid, Boat.bname, squery.c.reserve_count)
        .join(squery, Boat.bid == squery.c.bid)
        .filter(squery.c.reserve_count > 0)
        .all()
    )
    with engine.begin() as connection:
        result = connection.execute(
            """
                select boats.bid, boats.bname, reserves_groupped.reserve_count
                from boats
                left join (select bid, count(*) as reserve_count from reserves group by bid) reserves_groupped
                on boats.bid = reserves_groupped.bid
                where reserves_groupped.reserve_count > 0;
            """
        )
        assert list(result) == list(query)


# List those sailors who have reserved every red boat (list the id and the name).
def test_2(engine, session):
    red_boat_count = session.query(func.count()).filter(Boat.color == "red").subquery()
    red_boats = session.query(Boat.bid).filter(Boat.color == "red").subquery()
    sailor_boat_count = (
        session.query(Reserve.sid, label("reserve_count", func.count(Reserve.bid)))
        .filter(Reserve.bid.in_(red_boats))
        .group_by(Reserve.sid)
        .subquery()
    )
    query = (
        session.query(Sailor.sid, Sailor.sname)
        .join(sailor_boat_count, Sailor.sid == sailor_boat_count.c.sid)
        .filter(sailor_boat_count.c.reserve_count == red_boat_count)
        .all()
    )
    with engine.begin() as connection:
        result = connection.execute(
            """
                select s.sid, s.sname
                from sailors s,
                     (select r.sid, count(r.bid) as r_count
                      from reserves r
                      where r.bid in (select bid from boats where color = 'red')
                      group by r.sid) t
                where s.sid = t.sid
                and t.r_count = (select count(*) as red_boat_count
                   from boats b
                   where color = 'red');
            """
        )
    assert list(query) == list(result)


# List those sailors who have reserved only red boats.
def test_3(engine, session):
    red_boats = session.query(Boat.bid).filter(Boat.color == "red").subquery()
    squery = (
        session.query(Reserve.sid)
        .join(red_boats, Reserve.bid == red_boats.c.bid, isouter=True)
        .group_by(Reserve.sid)
        .having(func.sum(case([(red_boats.c.bid == None, 1)], else_=0)) == 0)
        .subquery()
    )
    query = session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.in_(squery)).all()
    with engine.begin() as connection:
        result = connection.execute(
            """
                select s.sid, s.sname
                from sailors s
                where s.sid in (select r.sid
                               from reserves r
                                        left join (select bid from boats where color = 'red') t on r.bid = t.bid
                               group by r.sid
                               having SUM(case when t.bid is NULL then 1 else 0 end) = 0);
            """
        )
    assert list(query) == list(result)


# For which boat are there the most reservations?
def test_4(engine, session):
    query = (
        session.query(Reserve.bid, label("reserve_count", func.count()))
        .group_by(Reserve.bid)
        .order_by(desc("reserve_count"))
        .limit(1)
        .all()
    )
    with engine.begin() as connection:
        result = connection.execute(
            """
                select bid, count(*) as reserve_count 
                from reserves
                group by bid
                order by reserve_count desc
                limit 1;
            """
        )
    assert list(result) == list(query)


def test_5(engine, session):
    red_boats = session.query(Boat.bid).filter(Boat.color == "red").subquery()
    squery = (
        session.query(Reserve.sid)
        .join(red_boats, Reserve.bid == red_boats.c.bid, isouter=True)
        .group_by(Reserve.sid)
        .having(func.sum(case([(red_boats.c.bid == None, 0)], else_=1)) > 0)
        .subquery()
    )
    query = (
        session.query(Sailor.sid, Sailor.sname).filter(Sailor.sid.notin_(squery)).all()
    )
    with engine.begin() as connection:
        result = connection.execute(
            """
                select sid, sname
                from sailors
                where sid not in (select r.sid
                                 from reserves r
                                          left join (select bid from boats where color = 'red') t on r.bid = t.bid
                                 group by r.sid
                                 having SUM(case when t.bid is NULL then 0 else 1 end) > 0);
            """
        )
    assert list(result) == list(query)


# Find the average age of sailors with a rating of 10
def test_6(engine, session):
    query = session.query(func.avg(Sailor.age)).filter(Sailor.rating == 10).all()
    with engine.begin() as connection:
        result = connection.execute("select avg(age) from sailors where rating = 10;")
        assert list(result) == list(query)


# For each rating, find the name and id of the youngest sailor
def test_7(engine, session):
    squery = (
        session.query(Sailor.rating, label("min_age", func.min(Sailor.age)))
        .group_by(Sailor.rating)
        .subquery()
    )
    query = (
        session.query(Sailor.rating, Sailor.sid, Sailor.sname, Sailor.age)
        .join(
            squery,
            and_(Sailor.rating == squery.c.rating, Sailor.age == squery.c.min_age),
        )
        .order_by(Sailor.rating)
        .all()
    )

    with engine.begin() as connection:
        result = connection.execute(
            """
                select s.rating, s.sid, s.sname, s.age
                from sailors s
                join (select rating, min(age) as min_age
                      from sailors
                      group by rating) t on s.rating = t.rating and s.age = t.min_age
                order by s.rating;
            """
        )
        assert list(result) == list(query)


# Select, for each boat, the sailor who made the highest number of reservations for that boat.
def test_8(engine, session):
    reserve1, reserve2 = aliased(Reserve), aliased(Reserve)
    squery = (
        session.query(
            reserve1.bid,
            label(
                "sid",
                session.query(reserve2.sid)
                .filter(reserve1.bid == reserve2.bid)
                .group_by(reserve2.sid)
                .order_by(desc(func.count()))
                .limit(1)
                .as_scalar(),
            ),
        )
        .group_by(reserve1.bid)
        .subquery()
    )
    query = (
        session.query(squery.c.bid, Sailor.sid, Sailor.sname)
        .join(squery, Sailor.sid == squery.c.sid)
        .order_by(squery.c.bid)
        .all()
    )
    with engine.begin() as connection:
        result = connection.execute(
            """
                select t.bid, t.sid, s.sname
                from sailors s
                        join
                    (select bid, (select sid from reserves where bid = r.bid group by sid order by count(*) desc limit 1) as sid
                     from reserves r
                     group by bid) t
                    on s.sid = t.sid
                order by t.bid asc;
            """
        )
        assert list(result) == list(query)


# Part C
# Bi-Weekly Payment given a start date
def test_9(engine, session):
    date_fomrat = "%Y-%m-%d"
    start_date_str = "1998-11-01"
    start_date_datetime = datetime.datetime.strptime(start_date_str, date_fomrat)
    end_date_datetime = start_date_datetime + datetime.timedelta(days=14)
    query = (
        session.query(Reserve.sid, Sailor.sname, func.sum(Reserve.price))
        .join(Sailor, Sailor.sid == Reserve.sid)
        .filter(
            and_(Reserve.day >= start_date_datetime, Reserve.day < end_date_datetime)
        )
        .group_by(Reserve.sid)
        .all()
    )
    assert (31, "lubber", 12) in query
    assert (23, "emilio", 2) in query


# Check available boats given a date (Daily Inventory Control)
def test_10(engine, session):
    date_fomrat = "%Y-%m-%d"
    date = "1998-11-06"
    date = datetime.datetime.strptime(date, date_fomrat)
    squery = session.query(Reserve.bid).filter(Reserve.day == date).subquery()
    query = session.query(Boat.bid, Boat.bname).filter(~Boat.bid.in_(squery)).all()
    query = list(map(lambda x: x[0], query))

    assert 103 not in query
    assert 105 not in query
    assert 110 not in query


# Check reserved boats given a date (Daily Inventory Control)
def test_11(engine, session):
    date_fomrat = "%Y-%m-%d"
    date = "1998-11-06"
    date = datetime.datetime.strptime(date, date_fomrat)
    squery = session.query(Reserve.bid).filter(Reserve.day == date).subquery()
    query = session.query(Boat.bid, Boat.bname).filter(Boat.bid.in_(squery)).all()
    query = list(map(lambda x: x[0], query))

    assert 103 in query
    assert 105 in query
    assert 110 in query


# Get a sorted list of boats with the highest number of reservations
def test_12(engine, session):
    query = (
        session.query(Reserve.bid, Boat.bname, func.count())
        .join(Boat, Boat.bid == Reserve.bid)
        .group_by(Reserve.bid)
        .order_by(desc(func.count()))
        .all()
    )
    assert (104, "Clipper", 5) == query[0]
    assert (109, "Driftwood", 4) == query[1]


# Get a sorted list of boats with the highest average rating
# if there is a tie in rating, order by the highest number of reservations
def test_13(engine, session):
    query = (
        session.query(
            Reserve.bid,
            Boat.bname,
            func.count(),
            label("boat_average_rating", func.avg(Reserve.rating)),
        )
        .filter(Reserve.rating != -1)
        .join(Boat, Boat.bid == Reserve.bid)
        .group_by(Reserve.bid)
        .order_by(desc("boat_average_rating"), desc(func.count()))
        .all()
    )

    assert (107, "Marine", 1, 5.0) == query[0]
    assert (103, "Clipper", 3, 4.0) == query[1]
    assert (106, "Marine", 3, 4.0) == query[2]
    assert (111, "Sooney", 1, 4.0) == query[3]


# Get a list of boats by location
def test_14(engine, session):
    location = 1
    query = session.query(Boat.bid, Boat.bname).filter(Boat.location == location).all()
    query = list(map(lambda x: x[0], query))

    assert 102 not in query
    assert 112 not in query


# Check reserved boats given a date and location (Daily Inventory Control)
def test_15(engine, session):
    date_fomrat = "%Y-%m-%d"
    date = "1998-11-06"
    location = 1
    date = datetime.datetime.strptime(date, date_fomrat)
    squery = session.query(Reserve.bid).filter(Reserve.day == date).subquery()
    query = (
        session.query(Boat.bid, Boat.bname)
        .filter(Boat.location == location)
        .filter(Boat.bid.in_(squery))
        .all()
    )
    query = list(map(lambda x: x[0], query))

    assert 103 in query


# Get sorted list of boasts with highest average rating
# when there is a tie in rating, order by highest number of reservation
# given a location
def test_16(engine, session):
    location = 1
    query = (
        session.query(
            Reserve.bid,
            Boat.bname,
            func.count(),
            label("boat_average_rating", func.avg(Reserve.rating)),
        )
        .filter(Reserve.rating != -1)
        .join(Boat, Boat.bid == Reserve.bid)
        .filter(Boat.location == location)
        .group_by(Reserve.bid)
        .order_by(desc("boat_average_rating"), desc(func.count()))
        .all()
    )

    assert (107, "Marine", 1, 5.0) == query[0]
    assert (103, "Clipper", 3, 4.0) == query[1]
    assert (106, "Marine", 3, 4.0) == query[2]
    assert (104, "Clipper", 5, 3.4) == query[3]
    assert (111, "Sooney", 1, 4.0) not in query
