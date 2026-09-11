import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.database import async_session_factory
from app.main import app
from app.models.wallets import Wallet


@pytest_asyncio.fixture
async def client():
    """Provide async HTTP client"""
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        yield client


@pytest_asyncio.fixture
async def wallet():
    """Create test wallet"""
    async with async_session_factory() as session:
        wallet = Wallet(balance=1000)
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)

        yield wallet

        await session.delete(wallet)
        await session.commit()
