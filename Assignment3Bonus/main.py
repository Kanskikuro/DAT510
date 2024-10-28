from transaction import Transaction
from blockchain import Blockchain
from wallet import Wallet

# Initialize the blockchain with a transaction limit
max_tx_per_block = 10
difficulty = 3 
blockchain = Blockchain(
    max_transactions_per_block=max_tx_per_block, difficulty=difficulty
)

# Create wallets for users
users = {}
for i in range(10):
    user_id = f"User_{i}"
    users[user_id] = Wallet()

# Generate and add 100 signed transactions
transactions = []  # Store all created transactions for testing
for i in range(1, 102):
    sender_id = f"User_{i % 10}"
    recipient_id = f"User_{(i + 1) % 10}"
    amount = i * 0.1
    sender_wallet = users[sender_id]
    recipient_wallet = users[recipient_id]

    transaction = sender_wallet.create_transaction(recipient_wallet.address, amount)
    transactions.append(transaction)  # Keep track of transactions

    # last transcation will be used to test the invalid case of the transcation inclusion.
    if i <= 100:
        if blockchain.add_transaction(transaction):
            print(f"Transaction {i} added: {transaction}")
        else:
            print(f"Transaction {i} is invalid and was discarded.")
