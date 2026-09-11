from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    """Operation type"""

    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperationRequest(BaseModel):
    """Wallet operation request"""

    operation_type: OperationType
    amount: Decimal = Field(gt=0)


class WalletResponse(BaseModel):
    """Wallet response"""

    id: UUID
    balance: Decimal
