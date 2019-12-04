from typing import AsyncGenerator

import asyncpg
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import Select

from asyncdb import model


def create_if_not_exists(create_table: CreateTable) -> str:
    return str(
        create_table.compile(
            dialect=postgresql.dialect()
        )
    ).replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)


class Database:

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def ensure_schema(self):
        async with self.pool.acquire() as con:
            # the first three tables can be created in any order, scheduling them as
            # tasks for asyncio.gather, but this method should only be called
            # on startup, so it shouldn't really matter
            await con.execute(
                create_if_not_exists(CreateTable(model.planets))
            )
            await con.execute(
                create_if_not_exists(CreateTable(model.races))
            )
            await con.execute(
                create_if_not_exists(CreateTable(model.starships))
            )
            await con.execute(
                create_if_not_exists(CreateTable(model.starship_count))
            )
            await con.execute(
                create_if_not_exists(CreateTable(model.planet_race))
            )

    async def insert_into_planets(self, planet_code: str):
        query = model.planets.insert().values(planet_code=planet_code)
        async with self.pool.acquire() as con:
            await con.execute(query)

    async def get_planets(self) -> AsyncGenerator[str, None]:
        query = Select(columns=[model.planets.columns.planet_code])
        async with self.pool.acquire() as con:
            for row in await con.fetch(query):
                yield row
