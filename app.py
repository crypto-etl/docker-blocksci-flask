import requests
from datetime import datetime
from flask import Flask, jsonify, request

import blocksci
from serializer import BlockSerializer, TransactionSerializer


blockchain = blocksci.Blockchain('/blocksci/blocksci-parser/')


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


@app.route('/block/<height>', methods=['GET'])
def serve_block(height):
    """
    returns a json serialized blocksci.Block object

    ------------------------
    Parameters passed in URL
    ------------------------

    param: height (int)
        block height
    """
    if not height.isdigit():
        return jsonify(data='Invalid argument: Block Height must be an integer')

    if int(height) > len(blockchain) - 1:
        return jsonify(data='Invalid argument: Block at given Height not found')

    block = blockchain[int(height)]
    return jsonify(data=BlockSerializer.serialize(block))


@app.route('/block/list', methods=['GET'])
def serve_block_list():
    """
    returns a list of json serialized blocksci.Block objects

    ---------------------------------
    Parameters passed in Request Body
    ---------------------------------

    param: start (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    param: end (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    """
    start, end = request.values.get('start'), request.values.get('end')

    if start is None or end is None:
        return jsonify(data='`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)
        return jsonify(data=[BlockSerializer.serialize(_block) for _block in blocks])
    except (IndexError, ValueError) as e:
        return jsonify(data=str(e))


@app.route('/transaction/<_hash>', methods=['GET'])
def serve_transaction(_hash):
    """
    returns a json serialized blocksci.Tx object

    ------------------------
    Parameters passed in URL
    ------------------------

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


@app.route('/transaction/list', methods=['GET'])
def serve_block_list():
    """
    returns a list of json serialized blocksci.Tx objects

    ---------------------------------
    Parameters passed in Request Body
    ---------------------------------

    param: start (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    param: end (int, str)
        block height or a string which can be parsed to a datetime.datetime object
    """
    start, end = request.values.get('start'), request.values.get('end')

    if start is None or end is None:
        return jsonify(data='`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)
        serialized_blocks = [BlockSerializer.serialize(_block) for _block in blocks]
        txes = [_serialized_block.txes for _serialized_block in serialized_blocks for _tx in _serialized_block.txes]
        # 2 for loops are present in order to flatten list of list to a list
        return jsonify(data=txes)
    except (IndexError, ValueError) as e:
        return jsonify(data=str(e))
