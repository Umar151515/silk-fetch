from typing import Unpack
from datetime import date

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from fastapi import Depends

from backend.src.core.dependencies import get_db_session
from backend.src.shared.orders.models import OrderDispatch, OrderDispatchArgs


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_dispatch(
            self,
            date_dispatch: date,
            track_number: str,
            client_code: str
        ) -> OrderDispatch:
        order_dispatch = OrderDispatch(
            track_number=track_number,
            date_dispatch=date_dispatch,
            client_code=client_code
        )
        self.session.add(order_dispatch)
        await self.session.flush()
        
        return order_dispatch

    async def delete_dispatch_by_id(self, dispatch_id: int) -> OrderDispatch | None:
        stmt = delete(OrderDispatch).where(OrderDispatch.id == dispatch_id).returning(OrderDispatch)
        result = await self.session.execute(stmt)
        await self.session.flush()

        return result.scalar_one_or_none()

    async def delete_dispatches_by_details(self, **kwargs: Unpack[OrderDispatchArgs]) -> int:
        if not kwargs:
            return 0

        stmt = delete(OrderDispatch).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        await self.session.flush()

        return result.rowcount
    
    async def upsert_dispatches(self, data: list[OrderDispatchArgs]) -> None:
        if not data:
            return

        stmt = insert(OrderDispatch)
        
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=[
                OrderDispatch.track_number,
                OrderDispatch.date_dispatch,
            ],
            set_={
                OrderDispatch.client_code: stmt.excluded.client_code
            }
        ) 

        await self.session.execute(upsert_stmt, data)
        await self.session.flush()

    async def get_dispatch_by_id(self, dispatch_id: int) -> OrderDispatch | None:
        return await self.session.get(OrderDispatch, dispatch_id)

    async def get_dispatches_by_details(
            self, 
            offset: int | None = None,
            limit: int | None = None, 
            **kwargs: Unpack[OrderDispatchArgs]
        ) -> list[OrderDispatch]:

        stmt = select(OrderDispatch).filter_by(**kwargs).offset(offset).limit(limit)

        result = await self.session.scalars(stmt)
        return result.all()

    async def update_dispatch_by_id(
            self,
            dispatch_id: int,
            **kwargs: Unpack[OrderDispatchArgs]
        ) -> OrderDispatch | None:
        if not kwargs:
            return None

        stmt = (
            update(OrderDispatch)
            .where(OrderDispatch.id == dispatch_id)
            .values(**kwargs)
            .returning(OrderDispatch)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()

        return result.scalar_one_or_none()

    async def update_dispatches_by_details(
            self,
            update_data: OrderDispatchArgs,
            **kwargs: Unpack[OrderDispatchArgs]
        ) -> int:
        if not update_data:
            return 0
        
        stmt = (
            update(OrderDispatch)
            .filter_by(**kwargs)
            .values(**update_data)
        )
        result = await self.session.execute(stmt)
        await self.session.flush()

        return result.rowcount

def get_order_repository(
        session: AsyncSession = Depends(get_db_session)
    ) -> OrderRepository:
    return OrderRepository(session)