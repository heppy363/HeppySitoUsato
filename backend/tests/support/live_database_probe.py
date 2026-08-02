from __future__ import annotations

import argparse
import asyncio
import json

from sqlalchemy import text

from app.core.config import get_settings
from app.database import DatabaseSessionManager


async def check_connection() -> None:
    manager = DatabaseSessionManager(get_settings().build_database_settings())
    try:
        await manager.check_connection()
        print("connection_ok")
    finally:
        await manager.dispose()


async def list_public_tables() -> None:
    manager = DatabaseSessionManager(get_settings().build_database_settings())
    try:
        async with manager.session() as session:
            result = await session.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                    """
                )
            )
            tables = list(result.scalars())
    finally:
        await manager.dispose()

    print(json.dumps({"tables": tables}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("connection", "public-tables"))
    args = parser.parse_args()

    if args.command == "connection":
        asyncio.run(check_connection())
        return

    asyncio.run(list_public_tables())


if __name__ == "__main__":
    main()
