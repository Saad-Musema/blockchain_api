from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from blockchain import Blockchain
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.exceptions import InvalidSignature

app = FastAPI()
blockchain = Blockchain()

class UTXO(BaseModel):
    txid: str
    index: int
    amount: float

class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float
    public_key: str
    signature: str
    input_utxos: List[UTXO]
    output_utxos: List[UTXO]


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
        # Validate transaction's inputs (UTXO)
        if not blockchain.is_valid_transaction(transaction.dict()):
            raise HTTPException(status_code=400, detail="Invalid transaction or UTXOs.")
        
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
