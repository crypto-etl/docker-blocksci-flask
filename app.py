import os
import pytz
import requests
from datetime import datetime
from dateutil import parser
from flask import Flask, jsonify, request

import blocksci
from serializer import BlockSerializer, TransactionSerializer


API_ENDPOINT_BLOCK = '/blocks/<height>'
API_ENDPOINT_BLOCK_LIST = '/blocks/list'
API_ENDPOINT_TRANSACTION = '/transactions/<_hash>'
API_ENDPOINT_TRANSACTION_LIST = '/transactions/list'
BLOCKSCI_PARSER_FILES_LOC = os.getenv('BLOCKSCI_PARSER_FILES_LOC')

blockchain = blocksci.Blockchain(BLOCKSCI_PARSER_FILES_LOC)

app = Flask(__name__)


def filter_blocks_by_datetime(start_time, end_time):
    """
    Returns a list of blocks where `block_time` is 
    greater than or equal to start_time and
    less than end_time
    """
    start_time = parser.parse(start_time).replace(tzinfo=pytz.utc)
    end_time = parser.parse(end_time).replace(tzinfo=pytz.utc)
    return blockchain.filter_blocks(lambda block: block.time >= start_time and block.time < end_start)


def get_blockrange(start, end):
    """
    returns a blocksci.BlockIterator with blocks within the
    indicated (start, end) block heights or block times

    param: start (int, str)
        block height or block times
    param: end (int, str)
        block height or block times
    """
    try:
        if start.isdigit() and end.isdigit():
            start, end = int(start), int(end)
            blocks = blockchain[start:end]  #  Blocksci does not raise an IndexError in case slice indexes are out of range
        elif isinstance(start, str) and end is None:
            blocks = blockchain.range(start=start)
        elif isinstance(start, str) and isinstance(end, str): 
            blocks = filter_blocks_by_datetime(start_time=start, end_time=end)
        else:
            raise ValueError('Allowed Values for `start` and `end` are `integers` and `date strings`')
    except IndexError:
        # Blocksci raises an IndexError in case start end_date is before date of genesis block
        raise IndexError('End Date or Start Date for range is prior to Genesis block')
    return blocks


@app.route(API_ENDPOINT_BLOCK, methods=['GET'])
def serve_block(height):
    """
    returns a json serialized blocksci.Block object

    param: height (int)
        block height
    """
    if not height.isdigit():
        return jsonify('Invalid argument: Block Height must be an integer')

    if int(height) > len(blockchain) - 1:
        return jsonify('Invalid argument: Block at given Height not found')

    block = blockchain[int(height)]
    return jsonify(BlockSerializer.serialize(block))


@app.route(API_ENDPOINT_BLOCK_LIST, methods=['GET'])
def serve_block_list():
    """
    returns a list of json serialized blocksci.Block objects

    param: start (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    param: end (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    """
    start, end = request.args.get('start'), request.args.get('end')

    if start is None:
        return jsonify('`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)
        return jsonify([BlockSerializer.serialize(_block) for _block in blocks])
    except (IndexError, ValueError) as e:
        return jsonify(str(e))


@app.route(API_ENDPOINT_TRANSACTION, methods=['GET'])
def serve_transaction(_hash):
    """
    returns a json serialized blocksci.Tx object

    param: _hash (str)
        Transaction Hash
    """
    if len(_hash) != 64:
        return jsonify('Invalid argument: TxHash must be 64 chars')

    try:
        tx = blockchain.tx_with_hash(_hash)
        return jsonify(TransactionSerializer.serialize(tx))
    except RuntimeError as e:
        return jsonify(str(e))


@app.route(API_ENDPOINT_TRANSACTION_LIST, methods=['GET'])
def serve_transaction_list():
    """
    returns a list of json serialized blocksci.Tx objects

    param: start (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    param: end (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    """
    start, end = request.args.get('start'), request.args.get('end')

    if start is None:
        return jsonify('`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)

        lists_txes = [_block.txes for _block in blocks]
        txes = [TransactionSerializer.serialize(_tx) for list_txes in lists_txes for _tx in list_txes]
        # 2 for loops are present in order to flatten list of list to a list
        return jsonify(txes)
    except (IndexError, ValueError) as e:
        return jsonify(str(e))
