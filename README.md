# docker-blocksci-flask

A lightweight flask application over BlockSci which exposes block and transaction data over http
```
docker run --rm -d 
           -e BLOCKSCI_PARSER_FILES_LOC=/blocksci/blocksci-parser/ 
           -v /blocksci:/blocksci 
           -p 8888:5000 
           -it merklescience/docker-blocksci-flask:latest
```
## Methods

### 1. /block/
Returns a json representation of blocksci.Block object
```
curl -G ip_address:8888/block/1
```
### 2. /block/list
Returns a list of json representation of blocksci.Block objects whose block-time falls within a range of block-heights or within a range of block-times

```
Use block-heights to define range
curl -G -d "start=1" -d "end=2"  ip_address:8888/block/list

Use block-times to define range
curl -G  ip_address:8888/block/list -d "start=2010-10-01" -d "end=2010-10-02"
```

### 3. /transaction/
Returns a json representation of blocksci.Tx object
```
curl -G ip_address:8888/transaction/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
```

### 4. /transaction/list
Returns a list of json representation of blocksci.Tx objects
```
Use block-heights to define range
curl -G -d "start=1" -d "end=2"  ip_address:8888/transaction/list

Use block-times to define range
curl -G  ip_address:8888/transaction/list -d "start=2010-10-01" -d "end=2010-10-02"
```

## Preparing output for load to bigquery

If we have one `block` JSON payload from server per line, clean it like this:
```
cat dirty.json | perl -ne 's/^{"data":\[//;s/\]}$//;print' | jq -cr 'del(.txes, .inputs, .change_output, .coinbase_tx.inputs, .coinbase_tx.op_return, .coinbase_tx.change_output)' | perl -ne 's/ \+0000//g;print' > clean.json
```
