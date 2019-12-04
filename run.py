import asyncio

import asyncpgsa

from asyncdb import database


planets = [
    "mars",
    "pluto",
    "venuse"
]


async def main():
    pool = await asyncpgsa.create_pool(
        host="127.0.0.1",
        port=5432,
        user="postgres",
        password="postgres",
        database="test"
    )
    db = database.Database(pool)
    await db.ensure_schema()
    tasks = []
    for planet in planets:
        tasks.append(db.insert_into_planets(planet))
    await asyncio.gather(*tasks)

    async for planet in db.get_planets():
        print(planet)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
