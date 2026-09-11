import asyncio
from decimal import Decimal

from app.core.database import async_session_factory
from app.models.wallets import Wallet


async def seed_wallets():
    """Create test wallets"""
    async with async_session_factory() as session:
        wallets = [
            Wallet(balance=Decimal("1000.00")),
            Wallet(balance=Decimal("5000.00")),
            Wallet(balance=Decimal("0.00")),
        ]

        session.add_all(wallets)
        await session.commit()

        for wallet in wallets:
            print(f"Wallet: {wallet.id}, balance: {wallet.balance}")


if __name__ == "__main__":
    asyncio.run(seed_wallets())
