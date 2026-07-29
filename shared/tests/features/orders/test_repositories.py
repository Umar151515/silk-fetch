from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import pytest

from shared.features.orders.models import OrderDispatch
from shared.features.orders.repositories import OrderRepository, OrderDispatchArgs


async def test_add_dispatch_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    
    date_dispatch = date(2026, 7, 14)
    track_number = "EJ984392UD93453"
    client_code = "A1876"

    new_dispach = await repo.add_dispatch(
        date_dispatch=date_dispatch,
        track_number=track_number,
        client_code=client_code
    )

    assert new_dispach.id is not None
    assert new_dispach.date_dispatch == date_dispatch
    assert new_dispach.track_number == track_number
    assert new_dispach.client_code == client_code
    
    stmt = select(OrderDispatch).where(OrderDispatch.id == new_dispach.id)
    db_record = await db_session.scalar(stmt)

    assert db_record is not None
    assert db_record.track_number == track_number

async def test_add_dispatch_duplicate_raises_integrity_error(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    
    date_dispatch = date(2026, 7, 14)
    track_number = "EJ984392UD93453"

    await repo.add_dispatch(
        date_dispatch=date_dispatch,
        track_number=track_number,
        client_code="A1876"
    )

    with pytest.raises(IntegrityError):
        await repo.add_dispatch(
            date_dispatch=date_dispatch,
            track_number=track_number,
            client_code="A1877"
        )


async def test_get_dispatch_by_id_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    
    date_dispatch = date(2026, 7, 14)
    track_number = "EJ984392UD93453"
    client_code = "A1876"

    new_dispach = await repo.add_dispatch(
        date_dispatch=date_dispatch,
        track_number=track_number,
        client_code=client_code
    )

    assert (await repo.get_dispatch_by_id(new_dispach.id)) == new_dispach

async def test_get_dispatches_by_details_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)

    date_dispatch = date(2026, 7, 16)
    track_number_1 = "EJ984392UD93454"
    track_number_2 = "EJ984392UD93455"
    
    data: list[OrderDispatchArgs] = [
        {
            "client_code": "A1876",
            "track_number": "EJ984392UD93453",
            "date_dispatch": date(2026, 7, 15),
        },
        {
            "client_code": "A1878",
            "track_number": track_number_1,
            "date_dispatch": date_dispatch,
        },
        {
            "client_code": "A1879",
            "track_number": track_number_2,
            "date_dispatch": date_dispatch,
        },
    ]

    await repo.upsert_dispatches(data)

    dispatches = await repo.get_dispatches_by_details(
        date_dispatch=date_dispatch
    )

    track_numbers = [dispatch.track_number for dispatch in dispatches]

    assert len(dispatches) == 2
    assert track_number_1 in track_numbers
    assert track_number_2 in track_numbers
    assert dispatches[0].date_dispatch == dispatches[1].date_dispatch
    assert dispatches[0].date_dispatch == date_dispatch


async def test_upsert_dispatches_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)

    data: list[OrderDispatchArgs] = [
        {
            "client_code": "A1876",
            "track_number": "EJ984392UD93453",
            "date_dispatch": date(2026, 7, 14),
        },

        {
            "client_code": "A1878",
            "track_number": "EJ984392UD93454",
            "date_dispatch": date(2026, 7, 15),
        },
        {
            "client_code": "A1879",
            "track_number": "EJ984392UD93454",
            "date_dispatch": date(2026, 7, 15),
        },
    ]

    await repo.upsert_dispatches(data)

    [dispatch_1] = await repo.get_dispatches_by_details(
        track_number=data[0]["track_number"],
        date_dispatch=data[0]["date_dispatch"]
    )
    
    assert dispatch_1

    assert dispatch_1.id is not None
    assert dispatch_1.date_dispatch == data[0]["date_dispatch"]
    assert dispatch_1.track_number == data[0]["track_number"]
    assert dispatch_1.client_code == data[0]["client_code"]

    [dispatch_2] = await repo.get_dispatches_by_details(
        track_number=data[1]["track_number"],
        date_dispatch=data[1]["date_dispatch"]
    )

    assert dispatch_2.id is not None
    assert dispatch_2.date_dispatch == data[1]["date_dispatch"]
    assert dispatch_2.track_number == data[1]["track_number"]
    assert dispatch_2.client_code == data[2]["client_code"]


async def test_delete_dispatch_by_id_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    
    date_dispatch = date(2026, 7, 14)
    track_number = "EJ984392UD93453"
    client_code = "A1876"

    new_dispach = await repo.add_dispatch(
        date_dispatch=date_dispatch,
        track_number=track_number,
        client_code=client_code
    )

    delete_dispach = await repo.delete_dispatch_by_id(new_dispach.id)

    assert delete_dispach.id == new_dispach.id
    assert delete_dispach.date_dispatch == date_dispatch
    assert delete_dispach.track_number == track_number
    assert delete_dispach.client_code == client_code

    stmt = select(OrderDispatch).where(OrderDispatch.id == new_dispach.id)
    db_record = await db_session.scalar(stmt)

    assert db_record is None
    assert await repo.delete_dispatch_by_id(new_dispach.id) is None

async def test_delete_dispatches_by_details_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)

    date_dispatch_1 = date(2026, 7, 15)
    date_dispatch_2 = date(2026, 7, 16)
    track_number = "EJ984392UD93453"
    client_code = "A1876"
    
    data: list[OrderDispatchArgs] = [
        {
            "client_code": client_code,
            "track_number": track_number,
            "date_dispatch": date_dispatch_1,
        },
        {
            "client_code": "A1878",
            "track_number": "EJ984392UD93454",
            "date_dispatch": date_dispatch_2,
        },
        {
            "client_code": "A1879",
            "track_number": "EJ984392UD93455",
            "date_dispatch": date_dispatch_2,
        },
    ]

    await repo.upsert_dispatches(data)

    delete_count = await repo.delete_dispatches_by_details(
        date_dispatch=date_dispatch_2
    )

    assert delete_count == 2

    dispatches = await repo.get_dispatches_by_details()
    assert len(dispatches) == 1
    assert dispatches[0].track_number == track_number

    delete_count = await repo.delete_dispatches_by_details(
        date_dispatch=date_dispatch_2
    )

    assert delete_count == 0


async def test_update_dispatch_by_id_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)
    
    date_dispatch = date(2026, 7, 14)
    track_number = "EJ984392UD93453"

    new_date_dispatch = date(2026, 7, 14)
    new_track_number = "EJ984392UD93453"

    dispach = await repo.add_dispatch(
        date_dispatch=date_dispatch,
        track_number=track_number,
        client_code="A1876"
    )

    update_dispach = await repo.update_dispatch_by_id(
        dispach.id,
        date_dispatch=new_date_dispatch,
        track_number=new_track_number
    )

    assert update_dispach.date_dispatch == new_date_dispatch
    assert update_dispach.track_number == new_track_number

async def test_update_dispatches_by_details_success(db_session: AsyncSession):
    repo = OrderRepository(db_session)

    date_dispatch_2 = date(2026, 7, 16)
    client_code = "A1876"

    update_data: OrderDispatchArgs = {
        "client_code": "A1878"
    }
    
    dispatch_1 = await repo.add_dispatch(
        date_dispatch=date(2026, 7, 15),
        track_number="EJ984392UD93453",
        client_code=client_code
    )

    dispatch_2 = await repo.add_dispatch(
        date_dispatch=date_dispatch_2,
        track_number="EJ984392UD93454",
        client_code="A1876"
    )

    dispatch_3 = await repo.add_dispatch(
        date_dispatch=date_dispatch_2,
        track_number="EJ984392UD93455",
        client_code="A1877"
    )

    update_count = await repo.update_dispatches_by_details(
        update_data=update_data,
        date_dispatch=date_dispatch_2
    )
    assert update_count == 2

    await db_session.refresh(dispatch_1)
    assert dispatch_1.client_code == client_code

    await db_session.refresh(dispatch_2)
    assert dispatch_2.client_code == update_data["client_code"]

    await db_session.refresh(dispatch_3)
    assert dispatch_3.client_code == update_data["client_code"]