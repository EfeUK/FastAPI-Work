import asyncio
from typing import Dict, Optional, Union
from fastapi.encoders import jsonable_encoder

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


class Account(BaseModel):
    name: str
    description: Optional[str] = None
    balance: float
    active: bool = True

class UpdateAccount(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    balance: Optional[float] = None
    active: Optional[bool] = None


app = FastAPI()

accounts = dict()


async def get_account(account_id: int) -> Optional[Account]:
    if account_id in accounts:
        return accounts[account_id]
    else:
        return None

#test for post
async def post_account(account_id: int, account: Account) -> Optional[Account]:
    if account_id in accounts:
        return None
    else:
        accounts[account_id] = account.dict()
        return accounts[account_id]

async def add_account(account_id: int, account: Account) -> Optional[Account]:
    if account_id in accounts:
        return None
    else:
        accounts[account_id] = account.dict()
        return accounts[account_id]


async def delete_account(account_id: int) -> Optional[bool]:
    if account_id in accounts:
        return True
    else:
        return None


@app.get("/healthz")
async def get_health(request: Request) -> Union[Optional[Dict], HTTPException]:
    return {"status": True}


@app.get("/accounts/{account_id}")
async def read_account(account_id: int):
    res = await get_account(account_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Account not found")
    else:
        return res

# post account test
@app.post("/accounts/{account_id}", status_code=201)
async def create_account(account_id: int, account: Account):
    res = await post_account(account_id, account)
    if res is None:
        raise HTTPException(status_code=409, detail="Account exists")
    else:
        return res

@app.put("/accounts/{account_id}", status_code=201)
async def update_account(account_id: int, account: UpdateAccount):
    update_account_encoded = jsonable_encoder(account)
    accounts[account_id] = update_account_encoded
    return update_account_encoded

@app.patch("/accounts/{account_id}", response_model=Account)
async def update_account(account_id: int, account: Account):
    stored_account_data = accounts.get(account_id)
    if stored_account_data is not None:
        stored_account_model = Account(**stored_account_data)
    else:
        stored_account_model = Account()
    update_data = account.dict(exclude_unset=True)
    updated_account = stored_account_model.copy(update=update_data)
    accounts[account_id] = jsonable_encoder(updated_account)
    return updated_account
        


@app.delete("/accounts/{account_id}", status_code=200)
async def remove_account(account_id: int):
    if account_id is None:
        raise HTTPException(status_code=404, detail="Account not found")
    del accounts[account_id]
    return {"msg": "Successful"}