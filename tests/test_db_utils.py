from unittest import mock

import pytest

from app.db_utils import insert_from_data, update_from_data


@pytest.mark.asyncio
async def test_insert_from_data():
    table = mock.Mock()
    db_session = mock.AsyncMock()

    result_id = await insert_from_data(table, {}, db_session)

    assert result_id
    table.insert().values.assert_called_once_with(id=result_id)
    assert db_session.execute.call_count == 1


@pytest.mark.asyncio
async def test_insert_from_data_without_id():
    table = mock.Mock()
    db_session = mock.AsyncMock()

    data = {"id": "value"}
    result_id = await insert_from_data(table, data, db_session)

    assert result_id == data["id"]
    table.insert().values.assert_called_once_with(id=data["id"])
    assert db_session.execute.call_count == 1


@pytest.mark.asyncio
async def test_update_from_data():
    table = mock.Mock()
    db_session = mock.AsyncMock()

    data = {"attr": "value"}
    await update_from_data(table, data, db_session)

    table.update().values.assert_called_once_with(**data)
    assert db_session.execute.call_count == 1
