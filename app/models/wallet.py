from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Wallet(Base):
    """Wallet model"""

    __tablename__ = "wallets"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
    )
