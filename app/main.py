from fastapi import FastAPI

from app.api.wallets import router as wallets_router

app = FastAPI(
    title="Wallet API",
    description="REST API for user wallets",
    version="1.0.0",
)

app.include_router(wallets_router)
