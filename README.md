# docker-blocksci-flask

A lightweight flask application over BlockSci which exposes block and transaction data over http

## Methods

## Block

### 1. Query for a Single Block
```
curl http://<IPAddress>:<FlaskPort>/block/<BlockHeight>

{
  "data": {
    "base_size": 285,
    "bits": 486604799,
    "coinbase_param": "b'\\x04\\xff\\xff\\x00\\x1d\\x01\\x04EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks'",
    "coinbase_tx": {
      "base_size": 204,
      "block_height": 0,
      "block_time": "2009-01-03 18:15:05 +0000",
      "change_output": null,
      "fee": 0,
      "fee_per_byte": 0,
      "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
      "index": 0,
      "input_count": 0,
      "input_value": 0,
      "inputs": [],
      "is_coinbase": true,
      "locktime": 0,
      "op_return": null,
      "output_count": 1,
      "output_value": 5000000000,
      "outputs": [
        {
          "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
          "address_type": "Pay to pubkey",
          "age": null,
          "block": 0,
          "index": 0,
          "sequence_num": null,
          "spending_tx": null,
          "spending_tx_index": null,
          "spent_tx": null,
          "spent_tx_index": null,
          "tx": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
          "tx_index": 0,
          "type": "tx-output",
          "value": 5000000000
        }
      ],
      "size_bytes": 204,
      "total_size": 204,
      "virtual_size": 204,
      "weight": 816
    },
    "fee": 0,
    "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "height": 0,
    "input_count": 0,
    "input_value": 0,
    "nonce": 2083236893,
    "output_count": 1,
    "output_value": 5000000000,
    "revenue": 5000000000,
    "size_bytes": 285,
    "time": "2009-01-03 18:15:05 +0000",
    "time_seen": null,
    "timestamp": 1231006505,
    "total_size": 285,
    "tx_count": 1,
    "txes": [
      {
        "base_size": 204,
        "block_height": 0,
        "block_time": "2009-01-03 18:15:05 +0000",
        "change_output": null,
        "fee": 0,
        "fee_per_byte": 0,
        "hash": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
        "index": 0,
        "input_count": 0,
        "input_value": 0,
        "inputs": [],
        "is_coinbase": true,
        "locktime": 0,
        "op_return": null,
        "output_count": 1,
        "output_value": 5000000000,
        "outputs": [
          {
            "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "address_type": "Pay to pubkey",
            "age": null,
            "block": 0,
            "index": 0,
            "sequence_num": null,
            "spending_tx": null,
            "spending_tx_index": null,
            "spent_tx": null,
            "spent_tx_index": null,
            "tx": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            "tx_index": 0,
            "type": "tx-output",
            "value": 5000000000
          }
        ],
        "size_bytes": 204,
        "total_size": 204,
        "virtual_size": 204,
        "weight": 816
      }
    ],
    "version": 1,
    "virtual_size": 285,
    "weight": 1140
  }
}
```

### Transaction
