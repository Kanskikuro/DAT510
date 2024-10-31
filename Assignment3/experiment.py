import time
import matplotlib.pyplot as plt
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


transaction_range = 1000
for i in range(1, transaction_range+1):
    sender_id = f"User_{i % 10}"
    recipient_id = f"User_{(i + 1) % 10}"
    amount = i * 0.1
    sender_wallet = users[sender_id]
    recipient_wallet = users[recipient_id]

    transaction = sender_wallet.create_transaction(recipient_wallet.address, amount)
    blockchain.add_transaction(transaction)

# Measure the time taken to mine blocks (verify and generate a block)

blocks_mined = 0

start_mine_time = time.time()
if blockchain.mine():
    blocks_mined += 1
end_mine_time = time.time()

mine_time = end_mine_time - start_mine_time
block_throughput = blocks_mined / mine_time

# Output mining results
print(f"Total mining time: {mine_time:.2f} seconds")
print(f"Block mining throughput: {block_throughput:.2f} blocks/second")


# Mining speed vs difficulity

difficulty_levels = range(1, 6)  # range of difficulty levels
mining_times = []

for difficulty in difficulty_levels:
    blockchain = Blockchain(max_transactions_per_block=max_tx_per_block, difficulty=difficulty)

    # Measure mining time
    print(f"Starting mining with difficulty {difficulty}...")
    start_time = time.time()
    blockchain.mine()
    mining_time = time.time() - start_time
    mining_times.append(mining_time)
    print(f"Difficulty {difficulty}: Mining took {mining_time:.2f} seconds.")

# Plotting the results
plt.plot(difficulty_levels, mining_times, marker='o')
plt.title("Mining Time vs. Difficulty")
plt.xlabel("Difficulty")
plt.ylabel("Mining Time (seconds)")
plt.grid(True)
plt.show()

