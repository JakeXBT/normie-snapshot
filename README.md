## normie-snapshot

## Running a Local Fork of Base

In order to run this script, you will need to fork the Base network at a specific block height, and expose this fork as a node on your local machine.

Anvil provides a way of achieving this:

```
anvil -f https://base.rpc.rug.ai/[API KEY]--fork-block-number 14949166 --port 8545
```
