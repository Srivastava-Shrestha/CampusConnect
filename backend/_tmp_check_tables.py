import asyncio
from sqlalchemy import text
from app.core.database import engine

async def main():
    async with engine.connect() as conn:
        r = await conn.execute(text(
            "select table_schema, table_name from information_schema.tables "
            "where table_type='BASE TABLE' order by table_schema, table_name"
        ))
        for row in r:
            print(row)
        r2 = await conn.execute(text("select current_database(), current_schema(), current_setting('search_path')"))
        for row in r2:
            print("ctx:", row)

asyncio.run(main())
