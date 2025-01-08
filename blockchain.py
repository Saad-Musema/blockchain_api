from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.exceptions import InvalidSignature
from hashlib import sha256
import time
import requests
from typing import List, Dict, Any


class Block:
    def __init__(self, index: int, transactions: List[Dict[str, Any]], timestamp: float, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self):
        # Initialize the blockchain with genesis block and difficulty for mining
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions: List[Dict[str, Any]] = []

    def create_genesis_block(self) -> Block:
        """The genesis block is the first block in the chain, with no transactions."""
        return Block(0, [], time.time(), "0")

    def get_last_block(self) -> Block:
        """Returns the last block in the chain."""
        return self.chain[-1]

    def mine_block(self):
        """Mines a block by adding pending transactions to the block, ensuring proof-of-work."""
        if not self.pending_transactions:
            return None

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.get_last_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []  # Clear pending transactions after mining
        return new_block

    def add_transaction(self, transaction: Dict[str, Any]):
        """Validates and adds a transaction to pending transactions."""
        if not self.is_valid_transaction(transaction):
            raise ValueError("Invalid transaction signature.")
        self.pending_transactions.append(transaction)

    def is_valid_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Validates that the transaction has a valid signature."""
        try:
            sender_public_key = serialization.load_pem_public_key(transaction["public_key"].encode())
            signature = decode_dss_signature(bytes.fromhex(transaction["signature"]))
            transaction_data = f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}".encode()
            sender_public_key.verify(signature, transaction_data, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    def add_block(self, block_data: Dict[str, Any]) -> bool:
        """Adds a new block to the chain if it is valid."""
        block = Block(
            index=block_data["index"],
            transactions=block_data["transactions"],
            timestamp=block_data["timestamp"],
            previous_hash=block_data["previous_hash"]
        )
        block.nonce = block_data["nonce"]
        block.hash = block.calculate_hash()

        if self.is_valid_block(block, self.get_last_block()):
            self.chain.append(block)
            return True
        return False

    def is_valid_block(self, block: Block, previous_block: Block) -> bool:
        """Validates a block, including checks for the hash, previous hash, and proof-of-work."""
        if block.previous_hash != previous_block.hash:
            return False
        if block.hash != block.calculate_hash():
            return False
        if not block.hash.startswith("0" * self.difficulty):
            return False
        return True



def submit_transaction(transaction_data):
        url = "http://127.0.0.1:8000/new_transaction"  # FastAPI backend URL

        try:
            response = requests.post(url, json=transaction_data)
            # Check if the response is OK (status code 200)
            if response.status_code == 200:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "detail": response.json().get("detail")}
        except requests.exceptions.RequestException as e:
            return {"status": "error", "detail": str(e)}