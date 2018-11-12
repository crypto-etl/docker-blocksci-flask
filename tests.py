import unittest
from mock import Mock

from serializer import BlockSerializer, TransactionSerializer


class TestAddressSerializer(unittest.TestCase):

    def setUp(self):
        self.pubkey_address = self._setup_pubkey()
        self.nulldata_address = self._nulldata_address()
        self.txn_input = self._setup_txn_input()
        self.txn_outputs = self._setup_txn_outputs()
        self.txn_output = self.txn_outputs[0]
        self.txn = self._setup_txn()
        self.block = self._setup_block()

    def _setup_pubkey(self):
        pubkey_address = Mock()
        pubkey_address.address_string = "12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX"
        pubkey_address.address_type = "Pay to pubkey"
        return pubkey_address

    def _setup_nulldata_address(self):
        nulldata_address = Mock()
        nulldata_address.address_string = None
        nulldata_address.address_type = "Null data"
        return nulldata_address
        
    def _setup_txn_input(self):
        txn_input = Mock()
        txn_input.address = "1BNwxHGaFbeUBitpjy2AsKpJ29Ybxntqvb"
        txn_input.address_type = "Pay to pubkey hash"
        txn_input.age = 941
        txn_input.block = 100000
        txn_input.sequence_num = 4294967295
        txn_input.spent_tx = "87a157f3fd88ac7907c05fc55e271dc4acdc5605d187d646604ca8c0e9382e03"
        txn_input.tx = "fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4"
        # txn_input.type = "tx-input"
        txn_input.value = 5000000000
        return txn_input

    def _setup_txn_outputs(self):
        txn_output_1.address = "1JqDybm2nWTENrHvMyafbSXXtTk5Uv5QAn",
        txn_output_1.address_type = "Pay to pubkey hash"
        txn_output_1.block = 100000
        txn_output_1.is_spent = True
        txn_output_1.spending_tx = "5aa8e36f9423ee5fcf17c1d0d45d6988b8a5773eae8ad25d945bf34352040009"
        txn_output_1.tx = "fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4"
        txn_output_1.type = "tx-output"
        txn_output_1.value = 556000000

        txn_output_2.address = "1EYTGtG4LnFfiMvjJdsU7GMGCQvsRSjYhx",
        txn_output_2.address_type = "Pay to pubkey hash"
        txn_output_2.block = 100000
        txn_output_2.is_spent = True
        txn_output_2.spending_tx = "220ebc64e21abece964927322cba69180ed853bb187fbc6923bac7d010b9d87a"
        txn_output_2.tx = "fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4"
        txn_output_2.type = "tx-output"
        txn_output_2.value = 4444000000
        return [txn_output_1, txn_output_2]

    def _setup_txn(self):
        txn = Mock()
        txn.base_size = 134
        txn.block_height = 1
        txn.block_time = "2009-01-09 02:54:25 +0000"
        txn.change_output = self.txn_outputs[1]
        txn.fee = 0
        txn.fee_per_byte = 0
        txn.hash = "0e3e2357e806b6cdb1f70b54c3a3a17b6714ee1f0e68bebb44a74b1efd512098"
        txn.index = 1
        txn.input_count = 1
        txn.input_value = 5000000000
        txn.inputs = [self.txn_input]
        txn.is_coinbase = True
        txn.locktime = 0
        txn.op_return = self.nulldata_address
        txn.output_count = 1
        txn.output_value = 5000000000
        txn.outputs = [self.txn_output]
        txn.size_bytes = 134
        txn.total_size = 134
        txn.virtual_size = 134
        txn.weight = 536
        return txn

    # def _setup_block(self):
    #   base_size":215
    #   bits":486604799
    #   coinbase_param":"b'\\x04\\xff\\xff\\x00\\x1d\\x01 '"
    #   coinbase_tx":{"base_size":134,"block_height":5,"block_time":"2009-01-09 03:23:48 +0000","change_output":null,"fee":0,"fee_per_byte":0,"hash":"63522845d294ee9b0188ae5cac91bf389a0c3723f084ca1025e7d9cdfe481ce1","index":5,"input_count":0,"input_value":0,"inputs":[],"is_coinbase":true,"locktime":0,"op_return":null,"output_count":1,"output_value":5000000000,"outputs":[{"address":"1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu","address_type":"Pay to pubkey","block":5,"is_spent":false,"spending_tx":null,"tx":"63522845d294ee9b0188ae5cac91bf389a0c3723f084ca1025e7d9cdfe481ce1","type":"tx-output","value":5000000000}],"size_bytes":134,"total_size":134,"virtual_size":134,"weight":536}
    #   fee":0
    #   hash":"000000009b7262315dbf071787ad3656097b892abffd1f95a1a022f896f533fc"
    #   height":5
    #   input_count":0
    #   input_value":0
    #   nonce":2011431709
    #   output_count":1
    #   output_value":5000000000
    #   revenue":5000000000
    #   size_bytes":215
    #   time":"2009-01-09 03:23:48 +0000"
    #   time_seen":null
    #   timestamp":1231471428
    #   total_size":215
    #   tx_count":1
    #   txes":[{"base_size":134,"block_height":5,"block_time":"2009-01-09 03:23:48 +0000","change_output":null,"fee":0,"fee_per_byte":0,"hash":"63522845d294ee9b0188ae5cac91bf389a0c3723f084ca1025e7d9cdfe481ce1","index":5,"input_count":0,"input_value":0,"inputs":[],"is_coinbase":true,"locktime":0,"op_return":null,"output_count":1,"output_value":5000000000,"outputs":[{"address":"1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu","address_type":"Pay to pubkey","block":5,"is_spent":false,"spending_tx":null,"tx":"63522845d294ee9b0188ae5cac91bf389a0c3723f084ca1025e7d9cdfe481ce1","type":"tx-output","value":5000000000}],"size_bytes":134,"total_size":134,"virtual_size":134,"weight":536}]
    #   version":1
    #   virtual_size":215
    #   weight":860
