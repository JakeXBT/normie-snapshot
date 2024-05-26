"""
This file contains rug.ai's Multicall contract client.

This client allows you to make multiple eth_call operations in a single call to an RPC node, increasing
the efficiency of data retrieval from the blockchain.
"""

import json
from web3 import Web3
from web3.contract import Contract

MULTICALL_CONTRACTS = {
    "ethereum": "0x969E7f3eF471942ea3e2424CCc39a1B01BBe17DB",
    "base": "0x65ed2E70bca5E993a8D90048FBB7D2bC5D49a77c",
    "arbitrum": "0x969E7f3eF471942ea3e2424CCc39a1B01BBe17DB",
    "blast": "0xE21D4D1a853Ef43A2aF09F6CfaA563c610aa17E8",
}

with open("files/Multicall.json", "r") as json_file:
    MULTICALL_ABI = json.load(json_file)


class Multicall:
    def __init__(self, w3: Web3, network):
        self.address = Web3.to_checksum_address(MULTICALL_CONTRACTS.get(network))
        self.abi = MULTICALL_ABI
        self.web3 = w3
        self.multicall = self.web3.eth.contract(address=self.address, abi=self.abi)

    def call(self, calls: list) -> list:
        data = self.multicall.functions.tryAggregate(False, calls).call()
        return data

    def create_call(self, contract: Contract, fn_name: str, args: list) -> tuple:
        return (contract.address, contract.encodeABI(fn_name=fn_name, args=args))
