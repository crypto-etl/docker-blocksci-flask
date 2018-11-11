import os
import requests
from datetime import datetime
from flask import Flask, jsonify, request

import blocksci
from serializer import BlockSerializer, TransactionSerializer


API_ENDPOINT_BLOCK = '/block/<height>'
API_ENDPOINT_BLOCK_LIST = '/block/list?start=<start>&end=<end>'
API_ENDPOINT_TRANSACTION = '/transaction/<_hash>'
API_ENDPOINT_TRANSACTION_LIST = '/transaction/list?start=<start>&end=<end>'
BLOCKSCI_PARSER_FILES_LOC = os.getenv('BLOCKSCI_PARSER_FILES_LOC')

blockchain = blocksci.Blockchain(BLOCKSCI_PARSER_FILES_LOC)

app = Flask(__name__)


def get_blockrange(start, end):
    """
    returns a blocksci.BlockIterator with blocks within the
    indicated (start, end) block heights or block times

    param: start (int, str)
        block height or block times
    param: end (int, str)
        block height or block times
    """
    if start.isdigit() and end.isdigit():
        start, end = int(start), int(end)
        blocks = blockchain[start:end]  #  Blocksci does not raise an IndexError in case slice indexes are out of range
    elif isinstance(start, str) and isinstance(end, str):
        blocks = blockchain.range(start=start, end=end)
        # Blocksci raises an IndexError in case start end_date is before date of genesis block
        raise IndexError('End Date for range is prior to Genesis block')
    else:
        raise ValueError('Allowed Values for `start` and `end` are `integers` and `date strings`')
    return blocks


@app.route(API_ENDPOINT_BLOCK, methods=['GET'])
def serve_block(height):
    """
    returns a json serialized blocksci.Block object

    param: height (int)
        block height
    """
    if not height.isdigit():
        return jsonify(data='Invalid argument: Block Height must be an integer')

    if int(height) > len(blockchain) - 1:
        return jsonify(data='Invalid argument: Block at given Height not found')

    block = blockchain[int(height)]
    return jsonify(data=BlockSerializer.serialize(block))


@app.route(API_ENDPOINT_BLOCK_LIST, methods=['GET'])
def serve_block_list(start, end):
    """
    returns a list of json serialized blocksci.Block objects

    param: start (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    param: end (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    """
    if start is None or end is None:
        return jsonify(data='`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)
        return jsonify(data=[BlockSerializer.serialize(_block) for _block in blocks])
    except (IndexError, ValueError) as e:
        return jsonify(data=str(e))


@app.route(API_ENDPOINT_TRANSACTION, methods=['GET'])
def serve_transaction(_hash):
    """
    returns a json serialized blocksci.Tx object

    param: _hash (str)
        Transaction Hash
    """
    if len(_hash) != 64:
        return jsonify(data='Invalid argument: TxHash must be 64 chars')

    try:
        tx = blockchain.tx_with_hash(_hash)
        return jsonify(data=TransactionSerializer.serialize(tx))
    except RuntimeError:
        return jsonify(data=str(e))


@app.route(API_ENDPOINT_TRANSACTION_LIST, methods=['GET'])
def serve_transaction_list(start, end):
    """
    returns a list of json serialized blocksci.Tx objects

    param: start (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    param: end (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    """
    if start is None or end is None:
        return jsonify(data='`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)
        serialized_blocks = [BlockSerializer.serialize(_block) for _block in blocks]
        txes = [_tx for _serialized_block in serialized_blocks for _tx in _serialized_block['txes']]
        # 2 for loops are present in order to flatten list of list to a list
        return jsonify(data=txes)
    except (IndexError, ValueError) as e:
        return jsonify(data=str(e))
