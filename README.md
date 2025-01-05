### **Blockchain API with FastAPI** 

---

#### **Short Description**  
This project implements a basic blockchain system with RESTful endpoints using FastAPI. The application supports mining new blocks, adding transactions with public/private key signatures, and sharing blockchain data among nodes. It demonstrates core blockchain concepts like proof-of-work, transaction validation, and block verification.

---

### **Table of Contents**  
1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Setup and Installation](#setup-and-installation)  
4. [Endpoints](#endpoints)  
5. [Key Management](#key-management)  
6. [Testing and Usage](#testing-and-usage)  
7. [Blockchain Concepts Demonstrated](#blockchain-concepts-demonstrated)  
8. [Future Improvements](#future-improvements)  
9. [License](#license)  

---

### **Introduction**  
This project builds a simple blockchain system and exposes essential functionalities through RESTful APIs using FastAPI. The blockchain supports basic consensus, proof-of-work for mining, and key-based transaction validation, showcasing the essentials of a decentralized ledger system.

---

### **Features**  
- Mine a new block with proof-of-work consensus.  
- Add new transactions signed with public/private key pairs for authenticity.  
- Validate and add received blocks from other nodes.  
- Query the complete blockchain ledger via the `/chain` endpoint.  
- Pythonic design using classes for the Blockchain and Block structures.  
- Secure transactions using elliptic curve cryptography (ECDSA).

---

### **Setup and Installation**  

1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd <repo_folder>
   ```

2. **Create a Python virtual environment** (optional but recommended):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # For Linux/Mac
   venv\Scripts\activate       # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn cryptography
   ```

4. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API Documentation**:  
   Open your browser at `http://127.0.0.1:8000/docs` for interactive Swagger documentation.

---

### **Endpoints**  

#### **1. `/chain` [GET]**  
Returns the current blockchain ledger.  
**Example Response**:  
```json
{
    "chain": [
        {
            "index": 0,
            "transactions": [],
            "timestamp": 1696565505.201,
            "previous_hash": "0",
            "nonce": 0,
            "hash": "e6e7..."
        }
    ]
}
```

#### **2. `/mine_block` [POST]**  
Mines a new block with pending transactions.  
**Example Response**:  
```json
{
    "message": "Block mined successfully!",
    "block": {
        "index": 1,
        "transactions": [...],
        "timestamp": 1696565605.348,
        "previous_hash": "e6e7...",
        "nonce": 4356,
        "hash": "0000a3f..."
    }
}
```

#### **3. `/new_transaction` [POST]**  
Accepts new transactions with the following structure:  
```json
{
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 10.5,
    "public_key": "<Alice's Public Key>",
    "signature": "<Digital Signature>",
    "input_utxos": [...],
    "output_utxos": [...]
}
```

#### **4. `/add_block` [POST]**  
Adds a block received from another node after validation.  
Request body:  
```json
{
    "index": 1,
    "transactions": [...],
    "timestamp": 1696565705.493,
    "previous_hash": "0000a3f...",
    "nonce": 4356
}
```

---

### **Key Management**  

#### **Generating Private and Public Keys**  
Run this script to generate a private-public key pair:
```python
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Generate Private Key
private_key = ec.generate_private_key(ec.SECP256R1())
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Generate Public Key
public_key = private_key.public_key()
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(f"Private Key:\n{pem_private.decode()}")
print(f"Public Key:\n{pem_public.decode()}")
```

#### **Signing Transactions**  
Use the private key to sign transactions:
```python
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.hazmat.primitives import hashes

# Example signing a message
message = b"Alice sends 10.5 BTC to Bob"
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
encoded_signature = signature.hex()
print(f"Signature: {encoded_signature}")
```

#### **Verifying Signatures**  
Use the sender's public key to verify transaction authenticity:
```python
from cryptography.exceptions import InvalidSignature

# Example verification
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("Signature is valid")
except InvalidSignature:
    print("Signature is invalid")
```

---

### **Testing and Usage**  

1. Start the server:  
   ```bash
   uvicorn main:app --reload
   ```

2. Use tools like [Postman](https://www.postman.com/) or the built-in `/docs` for interactive testing.

3. Add new transactions, mine blocks, or share blocks between nodes to create and extend your blockchain.

---

### **Blockchain Concepts Demonstrated**  
1. **Proof-of-Work**: Blocks are mined using a difficulty-adjusted proof-of-work algorithm.  
2. **Cryptographic Security**: Transactions are signed and validated using elliptic curve cryptography.  
3. **Decentralization**: New blocks can be accepted from other nodes if valid.  
4. **Integrity**: Blockchain integrity is enforced via hashing and previous block validation.

---

### **Future Improvements**  
- Add peer-to-peer communication for sharing the blockchain among multiple nodes.  
- Implement UTXO tracking and balances.  
- Add Merkle tree construction for efficient transaction validation.  
- Add more advanced consensus algorithms (e.g., Proof-of-Stake).

---

### **License**  
This project is released under the [MIT License](LICENSE).  

--- 
