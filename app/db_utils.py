from uuid import uuid4


async def insert_from_data(table, data, db_session):
    if not data.get("id"):
        data["id"] = uuid4().hex

    query = table.insert().values(**data)
    await db_session.execute(query)

    return data["id"]


async def update_from_data(table, data, db_session):
    query = table.update().values(**data)
    await db_session.execute(query)
