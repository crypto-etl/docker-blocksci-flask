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

### 1. /block/1
Returns a json representation of blocksci.Block object at block_height = 1
curl ip_address:8888/block/1

### 2. /block/list?start=10&end=20
Returns a list of json representation of blocksci.Block objects with block_heights between 10 to 20


### 3. /transaction/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
Returns a json representation of blocksci.Tx object with hash 0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098
curl ip_address:8888/transaction/0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098

### 4. /transaction/list
