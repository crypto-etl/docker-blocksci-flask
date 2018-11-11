from datetime import timezone

import blocksci


class BaseSerializer(object):

    @property
    def attributes(cls):
        raise NotImplementedError

    @classmethod
    def serialize_default(cls, field):
        return field

    @classmethod
    def serialize(cls, obj):
        payload = dict()

        for attribute in cls.attributes:
            serializer_method_name = 'serialize_{attribute}'.format(attribute=attribute)
            serializer_method = getattr(cls, serializer_method_name, cls.serialize_default)
            payload[attribute] = serializer_method(getattr(obj, attribute, None))
        return payload

    @classmethod
    def serialize_address(cls, _address):
        if isinstance(_address, (blocksci.PubkeyAddress,
                                blocksci.PubkeyHashAddress,
                                blocksci.WitnessPubkeyHashAddress,
                                blocksci.ScriptHashAddress,
                                blocksci.WitnessScriptHashAddress,
                                )):
            return str(_address.address_string)
        elif isinstance(_address, blocksci.MultisigAddress):
            return [str(_add.address_string) for _add in _address.addresses]
        else:
            return None

    @classmethod
    def serialize_address_type(cls, _address_type):
        return str(_address_type)


class TransactionInputOutputSerializer(BaseSerializer):
    """
    Converts a blocksci.Input or blocksci.Output object to a dictionary.
    All fields available in a Input/Output instance are available on the returned dictionary

    Field definitions can be found at
    https://citp.github.io/BlockSci/reference/chain/input.html
    https://citp.github.io/BlockSci/reference/chain/output.html
    """

    attributes = (
        'address',
        'address_type',
        'age',
        'block',
        'index',
        'sequence_num',
        'spent_tx_index',
        'tx',
        'tx_index',
        'value',
        'spent_tx',
        'spending_tx',
        'spending_tx_index',
    )

    @classmethod
    def serialize_block(cls, _block):
        return _block.height

    @classmethod
    def serialize_tx(cls, _tx):
        return str(_tx.hash)

    @classmethod
    def serialize_spent_tx(cls, _spent_tx):
        return str(_spent_tx.hash) if _spent_tx else None

    @classmethod
    def serialize_spending_tx(cls, _spending_tx):
        return str(_spending_tx.hash) if _spending_tx else None

    @classmethod
    def serialize(cls, obj):
        payload = super().serialize(obj)
        payload['type'] = 'tx-output' if payload['spent_tx'] is None else 'tx-input'
        return payload


class TransactionSerializer(BaseSerializer):
    """
    Converts a blocksci.Tx object to a dictionary.

    All fields available in a Tx instance (except include_output_of_type, outs,
    ins, time_seen, block and observed_in_mempool) are available on the returned dictionary

    Field definitions can be found at https://citp.github.io/BlockSci/reference/chain/tx.html
    """
    attributes = (
        'base_size',
        'block_height',
        'block_time',
        'change_output',
        'fee',
        'fee_per_byte',
        'hash',
        'index',
        'input_count',
        'input_value',
        'inputs',
        'is_coinbase',
        'locktime',
        'op_return',
        'output_count',
        'output_value',
        'outputs',
        'size_bytes',
        'total_size',
        'virtual_size',
        'weight'
    )

    @classmethod
    def serialize_block_time(cls, _block_time):
        return _block_time.replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z')

    @classmethod
    def serialize_fee_per_byte(cls, _method):
        return _method()

    @classmethod
    def serialize_inputs(cls, _inputs):
        return [TransactionInputOutputSerializer.serialize(_input) for _input in _inputs]

    @classmethod
    def serialize_outputs(cls, _outputs):
        return [TransactionInputOutputSerializer.serialize(_output) for _output in _outputs]

    @classmethod
    def serialize_hash(cls, _hash):
        return str(_hash)


class BlockSerializer(BaseSerializer):
    """
    Converts a blocksci.Block object to a dictionary.

    All fields available in a block instance (except time_seen, next_block, prev_block
    , inputs, outputs, miner and net_full_type_value) are available on the returned dictionary

    Field definitions can be found at https://citp.github.io/BlockSci/reference/chain/block.html
    """

    attributes = (
        'base_size',
        'bits',
        'coinbase_param',
        'coinbase_tx',
        'fee',
        'hash',
        'height',
        'input_count',
        'input_value',
        'nonce',
        'output_count',
        'output_value',
        'revenue',
        'size_bytes',
        'time',
        'time_seen',
        'timestamp',
        'total_size',
        'tx_count',
        'txes',
        'version',
        'virtual_size',
        'weight',
    )

    @classmethod
    def serialize_hash(cls, _hash):
        return str(_hash)

    @classmethod
    def serialize_time(cls, _time):
        return _time.replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %z')

    @classmethod
    def serialize_coinbase_tx(cls, _coinbase_tx):
        return TransactionSerializer.serialize(_coinbase_tx)

    @classmethod
    def serialize_txes(cls, _txes):
        return [TransactionSerializer.serialize(_tx) for _tx in _txes]

    @classmethod
    def serialize_coinbase_param(cls, _coinbase_param):
        return str(_coinbase_param)
