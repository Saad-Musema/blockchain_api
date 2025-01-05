from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.exceptions import InvalidSignature
from hashlib import sha256
import time
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
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions: List[Dict[str, Any]] = []

    def create_genesis_block(self) -> Block:
        return Block(0, [], time.time(), "0")

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def mine_block(self):
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
        self.pending_transactions = []  # Clear pending transactions
        return new_block

    def add_transaction(self, transaction: Dict[str, Any]):
        if not self.is_valid_transaction(transaction):
            raise ValueError("Invalid transaction signature.")
        self.pending_transactions.append(transaction)

    def is_valid_transaction(self, transaction: Dict[str, Any]) -> bool:
        try:
            sender_public_key = serialization.load_pem_public_key(transaction["public_key"].encode())
            signature = decode_dss_signature(bytes.fromhex(transaction["signature"]))
            transaction_data = f"{transaction['sender']}{transaction['receiver']}{transaction['amount']}".encode()
            sender_public_key.verify(signature, transaction_data, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False

    def add_block(self, block_data: Dict[str, Any]) -> bool:
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
        if block.previous_hash != previous_block.hash:
            return False
        if block.hash != block.calculate_hash():
            return False
        if not block.hash.startswith("0" * self.difficulty):
            return False
        return True
