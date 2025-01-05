from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from blockchain import Blockchain
import base64

app = FastAPI()
blockchain = Blockchain()


class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float
    public_key: str
    signature: str
    input_utxos: List[Dict[str, Any]]
    output_utxos: List[Dict[str, Any]]


@app.get("/chain")
def get_chain():
    return {"chain": [block.__dict__ for block in blockchain.chain]}


@app.post("/mine_block")
def mine_block():
    block = blockchain.mine_block()
    if block is None:
        raise HTTPException(status_code=400, detail="No transactions to mine.")
    return {"message": "Block mined successfully!", "block": block.__dict__}


@app.post("/new_transaction")
def add_transaction(transaction: Transaction):
    try:
        blockchain.add_transaction(transaction.dict())
        return {"message": "Transaction added successfully!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/add_block")
def add_block(block_data: Dict[str, Any]):
    success = blockchain.add_block(block_data)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid block.")
    return {"message": "Block added to the chain successfully!"}
