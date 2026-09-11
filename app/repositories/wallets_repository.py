from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallets import Wallet


class WalletRepository:
    """Repository for wallet database operations"""

    def __init__(self, session: AsyncSession):
        """Initialize wallet repository"""
        self.session = session

    async def get_by_id(self, wallet_id: UUID):
        """Get wallet by ID"""
        result = await self.session.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        return result.scalar_one_or_none()

    async def get_for_update(self, wallet_id: UUID):
        """Get wallet for update"""
        result = await self.session.execute(
            select(Wallet).where(Wallet.id == wallet_id).with_for_update()
        )
        return result.scalar_one_or_none()
