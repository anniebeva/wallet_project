from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_session
from app.repositories.wallets_repository import WalletRepository
from app.schemas.wallets import WalletOperationRequest, WalletResponse
from app.services.wallets_service import (
    InsufficientFundsError,
    WalletNotFoundError,
    WalletService,
)


router = APIRouter(
    prefix='/api/v1/wallets',
    tags=['wallets'],
)


@router.post('/{wallet_id}/operation', response_model=WalletResponse)
async def process_operation(
    wallet_id: UUID,
    operation: WalletOperationRequest,
    session: AsyncSession = Depends(get_session),
):
    """Process wallet operation"""
    repository = WalletRepository(session)
    service = WalletService(repository)

    try:
        return await service.process_operation(
            wallet_id,
            operation.operation_type,
            operation.amount,
        )
    except WalletNotFoundError:
        raise HTTPException(status_code=404, detail='Wallet not found')
    except InsufficientFundsError:
        raise HTTPException(status_code=400, detail='Insufficient funds')

@router.get('/{wallet_id}', response_model=WalletResponse)
async def get_wallet_balance(
    wallet_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get current wallet balance"""
    repository = WalletRepository(session)
    service = WalletService(repository)

    try:
        return await service.get_wallet(wallet_id)
    except WalletNotFoundError:
        raise HTTPException(status_code=404, detail='Wallet not found')
