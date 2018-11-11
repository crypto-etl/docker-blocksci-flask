# docker-blocksci-flask

A lightweight flask application over BlockSci which exposes block and transaction data over http
```
docker run --rm -d -e BLOCKSCI_PARSER_FILES_LOC=/blocksci/blocksci-parser/ -v /blocksci:/blocksci -p 8888:5000 -it merklescience/docker-blocksci-flask:latest
```
## Methods

### 1. /block
### 2. /block/list
### 3. /transaction
### 4. /transaction/list
