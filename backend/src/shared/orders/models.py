from typing import TypedDict
from datetime import date

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.core.database import Base


class OrderDispatch(Base):
    __tablename__ = "order_dispatch"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_dispatch: Mapped[date] = mapped_column(nullable=False)
    track_number: Mapped[str] = mapped_column(nullable=False)
    client_code: Mapped[str] = mapped_column(index=True)

    __table_args__ = (
        UniqueConstraint("track_number", "date_dispatch"),
    )


class OrderDispatchArgs(TypedDict, total=False):
    date_dispatch: date
    track_number: str
    client_code: str