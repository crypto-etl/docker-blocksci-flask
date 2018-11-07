from datetime import datetime

from djchoices import ChoiceItem, DjangoChoice
from flask import Flask, jsonify

import blocksci
from serializer import BlockSerializer


blockchain = blocksci.Blockchain('/blocksci/blocksci-parser/')


app = Flask(__name__)


def get_blockrange(start, end):
	if start.isdigit() and end.isdigit():
		start, end = int(start), int(end)
		blocks = blockchain[start:end]
	elif isinstance(start, str) and isinstance(end, (str, None)):
		blocks = blockchain.range(start=start, end=end)
	else:
		raise ValueError('Allowed Values for `start` and `end` are `integers` and `date strings`')
	return blocks


@app.route('/block/<height>', methods=['GET'])
def serve_block(height):
	try:
		return jsonify({'data': BlockSerializer.serialize(blockchain[height])})
	except:
		return jsonify({'data': 'Invalid argument: Block Height (only int & <max(block_height))'})


@app.route('/block/list', methods=['GET'])
def serve_block_list():
	start, end = request.values.get('start'), request.values.get('end')

	if start is None or end is None:
		return jsonify(message='`start` and `end` arguments must be passed in request data')
	
	try:
		blocks = get_blockrange(start=start, end=end)
	except ValueError as e:
		return jsonify(message=e.message)
	return jsonify([BlockSerializer.serialize(_block) for _block in blocks])


@app.route('/transactions', methods=['GET'])
def serve_transaction():
	pass