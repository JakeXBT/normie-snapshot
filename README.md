## normie-snapshot

The purpose of this repository is to check the balances of holders of the Normie token on Base prior to an exploit that occurred on 26th May 2024.

The script `main.py` does data fetching and outputs to `holder_snapshot.json` a file which contains the balances of addresses who have interracted with the Normie token prior to the snapshot block.

The code in `multicall.py` contains rug.ai's implementation of a client for optimized RPC calls.

The `/files` folder contains contract ABIs for `Multicall` and the standard ERC-20 token implementation.

## Running a Local Fork of Base

In order to run this script, you will need to fork the Base network at a specific block height, and expose this fork as a node on your local machine.

Anvil provides a way of achieving this:

```
anvil -f https://base.rpc.rug.ai/[API KEY]--fork-block-number 14949166 --port 8545
```
