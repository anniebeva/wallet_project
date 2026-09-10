from decimal import Decimal
from uuid import UUID

from app.repositories.wallets_repository import WalletRepository
from app.schemas.wallets import OperationType


class WalletNotFoundError(Exception):
    """Wallet was not found"""


class InsufficientFundsError(Exception):
    """Wallet has insufficient funds"""


class WalletService:
    """Service for wallet operations"""

    def __init__(self, repository: WalletRepository):
        """Initialize wallet service"""
        self.repository = repository

    async def get_wallet(self, wallet_id: UUID):
        """Get wallet by ID"""
        wallet = await self.repository.get_by_id(wallet_id)

        if wallet is None:
            raise WalletNotFoundError

        return wallet

    async def process_operation(
        self,
        wallet_id: UUID,
        operation_type: OperationType,
        amount: Decimal,
    ):
        """Process wallet operation"""
        async with self.repository.session.begin():
            wallet = await self.repository.get_for_update(wallet_id)

            if wallet is None:
                raise WalletNotFoundError

            if operation_type == OperationType.DEPOSIT:
                wallet.balance += amount

            elif operation_type == OperationType.WITHDRAW:
                if wallet.balance < amount:
                    raise InsufficientFundsError

                wallet.balance -= amount

        return wallet
