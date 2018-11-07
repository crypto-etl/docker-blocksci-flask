import json
from datetime import datetime
from flask import Flask, Response

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
    try:
        block = blockchain[height]
        response = {'data': BlockSerializer.serialize(block)}
    except:
        response = {'data': 'Invalid argument: Block Height (only int & <max(block_height))'}
    finally:
        return json.dumps(response), 200, 'application/json'


@app.route('/block/list', methods=['GET'])
def serve_block_list():
    start, end = request.values.get('start'), request.values.get('end')

    if start is None or end is None:
        response = {'data': '`start` and `end` arguments must be passed in request data'}
        return json.dumps(response), 200, 'application/json'
    
    try:
        blocks = get_blockrange(start=start, end=end)
    except ValueError as e:
        return json.dumps({'data': e.message}), 200, 'application/json'

    response = {'data': [BlockSerializer.serialize(_block) for _block in blocks]}
    return json.dumps(response), 200, 'application/json'


@app.route('/transactions', methods=['GET'])
def serve_transaction():
    pass