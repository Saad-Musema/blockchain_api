import streamlit as st
import requests
from key_signature_generator import generate_key_pair, sign_transaction 
from blockchain import submit_transaction

# Define the API base URL
API_BASE_URL = "http://127.0.0.1:8000"

def home_page():
     st.title("Welcome to Blockchain Explorer")
     st.write("""
            ## About the Project
            Blockchain Explorer is an interactive platform designed to showcase the functionality of a blockchain in a user-friendly environment. 
            Built with **Streamlit** for the front-end and **FastAPI** for the back-end, this project bridges the gap between complex blockchain technology and simple, interactive tools.

            ## Key Features
            - **View Blockchain Ledger**: Visualize blocks containing transaction details such as sender, receiver, amount, nonce, and hash values.
            - **Submit Transactions**: Add new transactions by providing the sender, receiver, amount, digital signature, and public key.
            - **Mine Blocks**: Combine pending transactions into new blocks through Proof-of-Work (PoW) mining.
            - **Validate Blocks**: Ensure chain integrity by verifying hashes and previous block links.
            - **Interactive UI**: Navigate with ease using a sidebar and intuitive page layouts.

            ## Educational Benefits
            This project is designed to:
            - Help users understand core blockchain concepts.
            - Illustrate cryptographic principles like public-private key cryptography and digital signatures.
            - Demonstrate how consensus mechanisms (e.g., PoW) validate and secure transactions.

            ## Technologies Used
            - **Python**: Core language for the project.
            - **FastAPI**: Provides scalable API endpoints for blockchain operations.
            - **Streamlit**: Powers the interactive, real-time interface.
            - **Cryptography Library**: Ensures secure key handling and transaction validation.

            ## Potential Applications
            - **Education**: Simplify blockchain teaching and training.
            - **Experimentation**: Test new blockchain features, algorithms, or consensus methods.
            - **Prototyping**: Adapt the platform as a foundation for real-world blockchain applications.

            ## Next Steps
            Planned future updates include:
            - Integration of smart contract functionality.
            - Support for multiple consensus algorithms (e.g., Proof-of-Stake).
            - Enhanced transaction visualization with charts and graphs.

            ## Useful Links
            - [Streamlit Documentation](https://docs.streamlit.io)
            - [FastAPI Documentation](https://fastapi.tiangolo.com)
            - [Cryptography Library Documentation](https://cryptography.io)

            Explore, interact, and learn with Blockchain Explorer!
        """)   
     
     st.title("How Transactions Work in a Blockchain")

     st.markdown("""
        ## What is a Blockchain Transaction?
        A blockchain transaction represents the transfer of digital value from one party to another on a blockchain network.
        It is a critical component of the blockchain, allowing users to exchange assets securely and transparently.

        ## Key Components of a Transaction
        Each transaction in our blockchain contains the following fields:

        - **Sender**: The address of the sender who initiates the transaction.
        - **Receiver**: The address of the receiver who will receive the funds.
        - **Amount**: The value (e.g., in cryptocurrency) being transferred.
        - **Public Key**: A cryptographic key associated with the sender, used to verify their identity.
        - **Signature**: A digital signature generated using the sender's private key, ensuring the authenticity and integrity of the transaction.
        - **Input UTXOs**: A list of "Unspent Transaction Outputs" (UTXOs) used as input to this transaction. UTXOs are outputs from previous transactions that the sender is spending.
        - **Output UTXOs**: A list of new outputs created by this transaction. These outputs will become new UTXOs for future transactions.

        ## How are Transactions Added?
        Here's the typical flow:
        1. **Transaction Creation**: The sender creates a transaction, specifying the sender address, receiver address, amount, and other fields.
        2. **Signature Generation**: The transaction is signed using the sender's private key.
        3. **Broadcast to Network**: The transaction is broadcast to the blockchain network (or, in our case, added to the pending transactions queue).
        4. **Verification**: The transaction signature is validated using the sender's public key.
        5. **Inclusion in a Block**: Once validated, the transaction is added to the next mined block.
        6. **Confirmation**: The mined block containing the transaction is appended to the blockchain, making the transaction immutable.

        ## Validation Process
        Validation ensures that:
        - The signature matches the public key.
        - The sender has sufficient balance (validated using input UTXOs).
        - No double-spending occurs (outputs can be spent only once).

        ## Why Transactions Need Signatures?
        Digital signatures ensure that transactions:
        - Originate from the real owner (authenticity).
        - Have not been altered during transmission (integrity).

     """)
    
     st.sidebar.success("Select a page to start exploring!")

def transaction_page():
    st.title("Submit a New Transaction")

    # Inputs for the transaction
    sender = st.text_input("Sender Address")
    receiver = st.text_input("Receiver Address")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    public_key = st.text_area("Sender's Public Key")
    signature = st.text_area("Digital Signature")
    input_utxos = st.text_area("Input UTXOs (as JSON)")
    output_utxos = st.text_area("Output UTXOs (as JSON)")

    if st.button("Submit Transaction"):
        try:
            transaction = {
                "sender": sender,
                "receiver": receiver,
                "amount": amount,
                "public_key": public_key,
                "signature": signature,
                "input_utxos": eval(input_utxos),
                "output_utxos": eval(output_utxos),
            }
            response = requests.post(f"{API_BASE_URL}/new_transaction", json=transaction)
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json()["detail"])
        except Exception as e:
            st.error(f"Error: {e}")

def mining_page():
    st.title("Mine a Block")

    if st.button("Mine Block"):
        response = requests.post(f"{API_BASE_URL}/mine_block")
        if response.status_code == 200:
            block = response.json()["block"]
            st.success("Block mined successfully!")
            st.json(block)
        else:
            st.error(response.json()["detail"])

def blockchain_viewer_page():
    st.title("View Blockchain Ledger")

    response = requests.get(f"{API_BASE_URL}/chain")
    if response.status_code == 200:
        chain = response.json()["chain"]
        st.write(f"Blockchain contains {len(chain)} blocks:")
        for block in chain:
            st.subheader(f"Block {block['index']}")
            st.json(block)
    else:
        st.error("Failed to retrieve the blockchain.")


def generate_key_signature_page():
    # Title of the page
    st.title("Generate Public Key & Signature")

    # Generate keys button
    if st.button("Generate Key Pair"):
        private_pem, public_pem = generate_key_pair()  # Generate key pair using the function

        # Store keys in session state
        st.session_state.private_key = private_pem
        st.session_state.public_key = public_pem

        # Display the keys to the user
        st.subheader("Private Key (PEM format)")
        st.text(private_pem)

        st.subheader("Public Key (PEM format)")
        st.text(public_pem)

        # Provide the transaction form for users to interact with
        sender = st.text_input("Sender Address", "Alice")
        receiver = st.text_input("Receiver Address", "Bob")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)

        # Transaction message based on user input
        transaction_message = f"{sender} sends {amount} to {receiver}"

        # Sign the transaction message if button is clicked
        if st.button("Sign Transaction"):
            # Ensure that private_key exists in the session state
            if "private_key" not in st.session_state:
                st.error("Private key not generated!")
                return  # Exit early if no private key was generated

            signature_hex = sign_transaction(st.session_state.private_key, transaction_message)

            # Displaying the details to the user
            st.subheader("Transaction Details")
            st.write(f"Sender: {sender}")
            st.write(f"Receiver: {receiver}")
            st.write(f"Amount: {amount}")
            st.write(f"Message: {transaction_message}")
            st.write(f"Signature (hex): {signature_hex}")
            st.write("**Note**: You can use this signature for validating transactions in the blockchain.")

        # Option for user to copy the signature
        if 'signature_hex' in locals():
            st.text_area("Copy the Signature", signature_hex, height=100)

def simulate_transaction_page():
    st.title("Generate Keys, Sign and Submit a Transaction")

    # Step 1: Generate Public and Private Keys
    if st.button("Generate Key Pair"):
        private_pem, public_pem = generate_key_pair()  # Call the key generation function

        # Store the keys in session state so they can be accessed later
        st.session_state.private_key = private_pem
        st.session_state.public_key = public_pem

        # Display the keys
        st.subheader("Private Key (PEM format)")
        st.text(private_pem)

        st.subheader("Public Key (PEM format)")
        st.text(public_pem)

    # Step 2: Input Transaction Details
    if 'private_key' in st.session_state:
        sender = st.text_input("Sender Address", "Alice")
        receiver = st.text_input("Receiver Address", "Bob")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)

        # Prepare the transaction message
        transaction_message = f"{sender} sends {amount} to {receiver}"

        st.subheader("Transaction Details")
        st.write(f"Sender: {sender}")
        st.write(f"Receiver: {receiver}")
        st.write(f"Amount: {amount}")
        st.write(f"Message: {transaction_message}")

        # Step 3: Sign the Transaction Message
        if st.button("Sign Transaction"):
            if "private_key" not in st.session_state:
                st.error("Private key is missing. Please generate the key pair first.")
            else:
                # Sign the transaction with the private key
                signature_hex = sign_transaction(st.session_state.private_key, transaction_message)
                
                # Store the signature in the session state
                st.session_state.signature = signature_hex

                st.subheader("Signature")
                st.write(f"Signature (hex): {signature_hex}")

                st.write("Now you can submit the transaction.")

                # Optionally display the keys again for the user
                st.subheader("Public Key (PEM format)")
                st.text(st.session_state.public_key)

                st.subheader("Private Key (PEM format)")
                st.text(st.session_state.private_key)

                # Step 4: Submit the Signed Transaction
            if st.button("Submit Transaction"):
                    # Construct the transaction object to send
                    transaction = {
                        "sender": sender,
                        "receiver": receiver,
                        "amount": amount,
                        "public_key": st.session_state.public_key,
                        "signature": st.session_state.signature,
                        "input_utxos": [{"txid": "some_txid", "index": 0, "amount": amount}],
                        "output_utxos": [{"txid": "new_txid", "index": 0, "amount": amount}],
                    }

                    # Send the transaction to the FastAPI backend
                    result = submit_transaction(transaction)

                    if result["status"] == "success":
                        st.success("Transaction submitted successfully!")
                        st.write("Transaction Details:", transaction)
                    else:
                        st.error(f"Transaction failed. {result['detail']}")

            st.write("**Note**: You can submit this transaction to the blockchain now.")


    else:
        st.write("Generate the key pair to continue.")


# Sidebar Navigation
PAGES = {
    "Home": home_page,
    "Submit Transaction": transaction_page,
    "Transaction Simulation": simulate_transaction_page,
    "Mine Block": mining_page,
    "View Blockchain": blockchain_viewer_page,
    
}

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", list(PAGES.keys()))
    PAGES[page]()

if __name__ == "__main__":
    main()
