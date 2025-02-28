from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3
import json
from typing import List, Optional

# FastAPI models
class UserRegistration(BaseModel):
    name: str
    email: str
    phone_number: str

class TokenIssuance(BaseModel):
    phone_number: str

class TokenRedemption(BaseModel):
    token_id: int

class UserInfoRequest(BaseModel):
    phone_number: str
    email: str

class TokenInfoRequest(BaseModel):
    token_id: int

# Connect to the local Hardhat node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
assert w3.is_connected(), "Failed to connect to node"

# Load contract ABI and address
with open('FoodTokenABI.json', 'r') as f:
    abi = json.load(f)

contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
contract = w3.eth.contract(address=contract_address, abi=abi)
sender = w3.eth.accounts[0]

# Create FastAPI app
app = FastAPI(title="Food Token API")

def main():
    # Sample data
    name = "John Doe"
    email = "john@example.com"
    phone_number = "3234567890"

    # Register user
    tx_hash = contract.functions.registerUser(name, email, phone_number).transact({'from': sender})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    registration_success = receipt['status'] == 1
    print(f"✅ User registration {'successful' if registration_success else 'failed'}")

    # Issue token
    tx_hash = contract.functions.issueToken(phone_number).transact({'from': sender})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Get token ID from event logs
    event_logs = contract.events.TokenIssued().process_receipt(receipt)
    token_id = event_logs[0]['args']['tokenId']
    print(f"✅ Token issued - ID: {token_id}")

    # Redeem token
    tx_hash = contract.functions.redeemToken(token_id).transact({'from': sender})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Token redeemed")

    # Get user info
    user_info = contract.functions.getUserInfo(phone_number, email).call()
    print("\nUser Info:")
    print(f"Name: {user_info[0]}")
    print(f"Email: {user_info[1]}")
    print(f"Phone: {user_info[2]}")
    print(f"Token IDs: {user_info[3]}")
    print(f"Exists: {user_info[4]}")

    # Get token info
    token_info = contract.functions.getTokenInfo(token_id).call()
    print("\nToken Info:")
    print(f"Exists: {token_info[0]}")
    print(f"Redeemed: {token_info[1]}")
    print(f"Creation Time: {token_info[2]}")
    print(f"Owner Phone: {token_info[3]}")

# FastAPI endpoints
@app.post("/register")
async def register_user(user: UserRegistration):
    try:
        tx_hash = contract.functions.registerUser(
            user.name,
            user.email,
            user.phone_number
        ).transact({'from': sender})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        success = receipt['status'] == 1
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/issue-token")
async def issue_token(request: TokenIssuance):
    try:
        tx_hash = contract.functions.issueToken(request.phone_number).transact({'from': sender})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        event_logs = contract.events.TokenIssued().process_receipt(receipt)
        token_id = event_logs[0]['args']['tokenId']
        return {"token_id": token_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/redeem-token")
async def redeem_token(request: TokenRedemption):
    try:
        tx_hash = contract.functions.redeemToken(request.token_id).transact({'from': sender})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return {"success": receipt['status'] == 1}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/user-info")
async def get_user_info(request: UserInfoRequest):
    try:
        user_info = contract.functions.getUserInfo(
            request.phone_number,
            request.email
        ).call()
        return {
            "name": user_info[0],
            "email": user_info[1],
            "phone_number": user_info[2],
            "token_ids": user_info[3],
            "exists": user_info[4]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/token-info/{token_id}")
async def get_token_info(token_id: int):
    try:
        token_info = contract.functions.getTokenInfo(token_id).call()
        return {
            "exists": token_info[0],
            "is_redeemed": token_info[1],
            "creation_time": token_info[2],
            "owner_phone": token_info[3]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# if __name__ == "__main__":
#     main()