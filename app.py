from datetime import datetime
from flask import Flask, jsonify, request

import blocksci
from serializer import BlockSerializer


blockchain = blocksci.Blockchain('/blocksci/blocksci-parser/')


app = Flask(__name__)


def get_blockrange(start, end):
    if start.isdigit() and end.isdigit():
        start, end = int(start), int(end)
        blocks = blockchain[start:end]
    elif isinstance(start, str) and isinstance(end, str):
        blocks = blockchain.range(start=start, end=end)
    else:
        raise ValueError('Allowed Values for `start` and `end` are `integers` and `date strings`')
    return blocks


@app.route('/block/<height>', methods=['GET'])
def serve_block(height):
    if not height.isdigit():
        return jsonify(data='Invalid argument: Block Height must be an integer')

    if int(height) > len(blockchain) - 1:
        return jsonify(data='Invalid argument: Block at given Height not found')        

    block = blockchain[int(height)]        
    return jsonify(data=BlockSerializer.serialize(block))


@app.route('/block/list', methods=['GET'])
def serve_block_list():
    start, end = request.values.get('start'), request.values.get('end')

    if start is None or end is None:
        return jsonify(data='`start` and `end` arguments must be passed in request data')

    try:
        blocks = get_blockrange(start=start, end=end)
    except ValueError as e:
        return jsonify(data=e.message)
    return jsonify(data=[BlockSerializer.serialize(_block) for _block in blocks])


@app.route('/transactions', methods=['GET'])
def serve_transaction():
    pass


if __init__