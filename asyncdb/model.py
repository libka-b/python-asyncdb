from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey
from sqlalchemy.schema import Sequence


metadata = MetaData()


planet_seq = Sequence("my_awesome_seq", start=1, increment=1)


planets = Table(
    "planets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("planet_code", String, unique=True, index=True),
)


races = Table(
    "races",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("race", String, unique=True)
)


starships = Table(
    "starship",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("starship_type", String, unique=True)
)


starship_count = Table(
    "starship_count",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("starship_type_id", Integer, ForeignKey("starship.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("count", Integer, default=0)
)


planet_race = Table(
    "planet_race",
    metadata,
    Column("planet_id", Integer, ForeignKey("planets.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("race_id", Integer, ForeignKey("races.id", onupdate="CASCADE", ondelete="CASCADE")),
    Column("starship_count_id", Integer, ForeignKey("starship_count.id", onupdate="CASCADE", ondelete="CASCADE"))
)
