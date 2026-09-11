from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_get_wallet(client, wallet):
    """Get existing wallet"""
    response = await client.get(f'/api/v1/wallets/{wallet.id}')

    assert response.status_code == 200
    assert response.json()['id'] == str(wallet.id)
    assert response.json()['balance'] == '1000.00'


@pytest.mark.asyncio
async def test_get_wallet_not_found(client):
    """Return 404 for missing wallet"""
    wallet_id = uuid4()

    response = await client.get(f'/api/v1/wallets/{wallet_id}')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Wallet not found'


@pytest.mark.asyncio
async def test_deposit(client, wallet):
    """Deposit funds into wallet"""
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        json={
            'operation_type': 'DEPOSIT',
            'amount': 500,
        },
    )

    assert response.status_code == 200
    assert response.json()['balance'] == '1500.00'


@pytest.mark.asyncio
async def test_withdraw(client, wallet):
    """Withdraw funds from wallet"""
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        json={
            'operation_type': 'WITHDRAW',
            'amount': 300,
        },
    )

    assert response.status_code == 200
    assert response.json()['balance'] == '700.00'


@pytest.mark.asyncio
async def test_insufficient_funds(client, wallet):
    """Reject withdrawal with insufficient funds"""
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        json={
            'operation_type': 'WITHDRAW',
            'amount': 1500,
        },
    )

    assert response.status_code == 400
    assert response.json()['detail'] == 'Insufficient funds'


@pytest.mark.asyncio
async def test_operation_wallet_not_found(client):
    """Return 404 for operation on missing wallet"""
    wallet_id = uuid4()

    response = await client.post(
        f'/api/v1/wallets/{wallet_id}/operation',
        json={
            'operation_type': 'DEPOSIT',
            'amount': 500,
        },
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'Wallet not found'


@pytest.mark.asyncio
async def test_invalid_amount(client, wallet):
    """Reject non-positive amount"""
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        json={
            'operation_type': 'DEPOSIT',
            'amount': 0,
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_operation_type(client, wallet):
    """Reject invalid operation type"""
    response = await client.post(
        f'/api/v1/wallets/{wallet.id}/operation',
        json={
            'operation_type': 'INVALID',
            'amount': 100,
        },
    )

    assert response.status_code == 422
