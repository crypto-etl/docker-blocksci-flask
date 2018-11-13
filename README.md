# docker-blocksci-flask

A lightweight flask application over BlockSci which exposes block and transaction data over http
```
docker run --rm -d 
           -e BLOCKSCI_PARSER_FILES_LOC=/blocksci/bitcoin.cfg 
           -v /blocksci:/blocksci 
           -p 5000:5000 
           -it merklescience/docker-blocksci-flask:latest
```
## Methods

### 1. /block/
Returns a json representation of blocksci.Block object
```
curl -G http://0.0.0.0:5000/block/1
```
### 2. /block/list
Returns a list of json representation of blocksci.Block objects whose block-time falls within a range of block-heights or within a range of block-times

```
Use block-heights to define range
curl -G -d "start=1" -d "end=2"  http://0.0.0.0:5000/block/list

Use block-times to define range
curl -G  http://0.0.0.0:5000/block/list -d "start=2010-10-01" -d "end=2010-10-02"
```

### 3. /transaction/
Returns a json representation of blocksci.Tx object
```
curl -G http://0.0.0.0:5000/transaction/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
```

### 4. /transaction/list
Returns a list of json representation of blocksci.Tx objects
```
Use block-heights to define range
curl -G -d "start=1" -d "end=2"  http://0.0.0.0:5000/transaction/list

Use block-times to define range
curl -G  http://0.0.0.0:5000/transaction/list -d "start=2010-10-01" -d "end=2010-10-02"
```

## Preparing output for load to bigquery

If we have `block` JSON payloads from server, one per line, clean it like this:
```
cat dirtyblock.json | perl -ne 's/^{"data":\[//;s/\]}$//;print' | jq -cr 'del(.txes, .inputs, .change_output, .coinbase_tx.inputs, .coinbase_tx.op_return, .coinbase_tx.change_output)' | perl -ne 's/ \+0000//g;print' > cleanblock.json
bq load --replace --source_format NEWLINE_DELIMITED_JSON dataset.blocktable cleanblock.json bigquery/schema/blocks.json
```

If we have `transaction` JSON payloads from server, one per line, clean it like this:
```
cat dirtytx.json | perl -ne 's/^{"data":\[//;s/\]}$//;s/ \+0000//g;print' > cleantx.json
bq load --replace --source_format NEWLINE_DELIMITED_JSON dataset.txtable cleantx.json bigquery/schema/transactions.json

```
