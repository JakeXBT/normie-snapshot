from web3 import Web3, HTTPProvider
import json

from multicall import Multicall

# Constants for analysis
NORMIE_TOKEN_ADDRESS = "0x7F12d13B34F5F4f0a9449c16Bcd42f0da47AF200"

with open("files/ERC20.json", "r") as f:
    ERC20_ABI = json.load(f)

# Create a Web3 instance pointing at the local Anvil fork of Base
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(HTTPProvider("https://base.llamarpc.com"))

NORMIE_TOKEN = w3.eth.contract(address=NORMIE_TOKEN_ADDRESS, abi=ERC20_ABI)
NORMIE_DECIMALS = NORMIE_TOKEN.functions.decimals().call()
NORMIE_RESCALING_FACTOR = 10**NORMIE_DECIMALS

# Create a Multicall instance for the Base network
multicall = Multicall(w3, "base")

current_block = w3.eth.block_number

# Step 1: Find all transfers of the token to identify a list of candidate holders to check
transfers = []

batch_size = 10000  # Number of blocks to fetch in each batch


def fetch_transfer_events(start_block, end_block):
    try:
        events = NORMIE_TOKEN.events.Transfer.get_logs(
            fromBlock=start_block, toBlock=end_block
        )
        return events
    except Exception as e:
        print(f"Error fetching logs from block {start_block} to {end_block}: {e}")
        return []


while current_block > w3.eth.block_number - 10000:
    from_block = max(0, current_block - batch_size)
    to_block = current_block
    pool_created_events = fetch_transfer_events(from_block, to_block)

    for event in pool_created_events:
        try:
            transfer_data = {
                "from": event["args"]["from"],
                "to": event["args"]["to"],
                "numTokens": event["args"]["value"] / NORMIE_RESCALING_FACTOR,
                "blockNumber": event["blockNumber"],
            }
            transfers.append(transfer_data)
        except Exception as e:
            pass  # Ignore errors and continue

    print(f"Processed blocks from {from_block} to {to_block}")
    current_block = from_block - 1

print(f"Total number of transfers: {len(transfers)}")


# Step 2: Fetch the lis of all addresses involved in the transfers
addresses = set()

for transfer in transfers:
    addresses.add(transfer["from"])
    addresses.add(transfer["to"])

addresses = list(addresses)

# Step 3: Fetch the balances of all addresses in a single multicall
# TODO: Batch these calls to avoid hitting the gas limit
calls = [
    multicall.create_call(
        NORMIE_TOKEN,
        "balanceOf",
        args={"_owner": w3.to_checksum_address(address)},
    )
    for address in addresses
]

balances = multicall.call(calls)

# Reformat the balances
balances = [
    max(int.from_bytes(item[1], "big") / NORMIE_RESCALING_FACTOR, 0)
    if item[0]
    else None
    for item in balances
]

print(f"Fetched balances for {len(balances)} addresses")
print(f"Number of calls made: {len(calls)}")

# Step 4: Combine the balances with the addresses
address_balances = [
    {"address": address, "balance": balance}
    for address, balance in zip(addresses, balances)
]

# Step 5: Export to a JSON file
with open("holder_snapshot.json", "w") as f:
    json.dump(address_balances, f)
