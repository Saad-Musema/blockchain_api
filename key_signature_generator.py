# key_signature_generator.py
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def generate_key_pair():
    """
    Generates a new private key and its corresponding public key.
    Returns:
        private_pem (str): Private key in PEM format
        public_pem (str): Public key in PEM format
    """
    private_key = ec.generate_private_key(ec.SECP256R1())  # ECDSA private key
    public_key = private_key.public_key()

    # Serialize keys to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()

def sign_transaction(private_key_pem, transaction_message):
    """
    Signs the transaction message using the private key.
    Args:
        private_key_pem (str): Private key in PEM format
        transaction_message (str): Transaction message to sign
    Returns:
        signature_hex (str): The hexadecimal format of the generated signature
    """
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    signature = private_key.sign(
        transaction_message.encode(),
        ec.ECDSA(hashes.SHA256())
    )

    return signature.hex()
