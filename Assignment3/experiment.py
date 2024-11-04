import time
import matplotlib.pyplot as plt
from blockchain import Blockchain
from wallet import Wallet

# Initialize the blockchain with a transaction limit ########################################################
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



#Measure the time taken to mine blocks (verify and generate a block) #####################################################################################################

# blocks_mined = 0

# start_mine_time = time.time()
# if blockchain.mine():
#     blocks_mined += 1
# end_mine_time = time.time()

# mine_time = end_mine_time - start_mine_time
# block_throughput = blocks_mined / mine_time

# # Output mining results
# print(f"Total mining time: {mine_time:.2f} seconds")
# print(f"Block mining throughput: {block_throughput:.2f} blocks/second")


# Mining speed vs difficulity ################################################################################################################################################
 
difficulty_levels = range(1, 1)  # range of difficulty levels
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

# Define the max transactions per block to test ##################################################################################################################################################################
max_tx_per_block_values = [1, 5, 10, 20, 50, 100, 500, 1000]
transaction_range = 100
performance_times = []

# Loop over each max_tx_per_block value
for max_tx in max_tx_per_block_values:
    difficulty = 3
    blockchain = Blockchain(max_transactions_per_block=max_tx, difficulty=difficulty)
    
    #users = {f"User_{i}": Wallet() for i in range(10)}
    
     # Create new transactions to mine
    for i in range(1, transaction_range + 1):
        sender_id = f"User_{i % 10}"
        recipient_id = f"User_{(i + 1) % 10}"
        amount = i * 0.1
        sender_wallet = users[sender_id]
        recipient_wallet = users[recipient_id]

        transaction = sender_wallet.create_transaction(recipient_wallet.address, amount)
        blockchain.add_transaction(transaction)

    start_time = time.time()
    blockchain.mine()
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    performance_times.append(elapsed_time)
    
    print(f"Max TX per block: {max_tx}, Time taken: {elapsed_time:.4f} seconds")

# Plotting the results | Doesnt lok good when the range it too big
# plt.figure(figsize=(10, 5))
# plt.plot(max_tx_per_block_values, performance_times, marker='o')
# plt.title('Blockchain Performance with Varying Max Transactions per Block')
# plt.xlabel('Max Transactions per Block')
# plt.ylabel('Time Taken (seconds)')
# plt.xticks(max_tx_per_block_values)
# plt.grid()
# plt.show()