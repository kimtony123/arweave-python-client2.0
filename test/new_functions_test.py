import unittest
from tempfile import TemporaryFile
import os
import json
from cryptography.fernet import Fernet
from flask import logging
from arweave import Wallet, Transaction, ArweaveTransactionException, Utils
from jose.utils import base64url_encode, base64url_decode, base64

class TestWalletAndTransaction(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet('jwk_file.json')
        self.test_data = "This is test data"
        self.transaction = Transaction(self.wallet, data=self.test_data)

    # Wallet tests
    def test_wallet_init(self):
        self.assertIsNotNone(self.wallet.jwk)
        self.assertIsNotNone(self.wallet.rsa)
        self.assertIsNotNone(self.wallet.owner)
        self.assertIsNotNone(self.wallet.address)

    def test_wallet_from_data(self):
        with open('jwk_file.json', 'r') as f:
            jwk_data = json.load(f)
        wallet_from_data = Wallet.from_data(jwk_data)
        self.assertEqual(self.wallet.address, wallet_from_data.address)

    def test_wallet_balance(self):
        try:
            balance = self.wallet.balance
            self.assertIsNotNone(balance)
            self.assertGreaterEqual(balance, 0)
        except ArweaveTransactionException:
            self.fail("ArweaveTransactionException was raised unexpectedly.")

    def test_wallet_sign(self):
        message = b"test message"
        signature = self.wallet.sign(message)
        self.assertIsNotNone(signature)

    def test_wallet_get_last_transaction_id(self):
        last_tx = self.wallet.get_last_transaction_id()
        self.assertIsNotNone(last_tx)

    def test_wallet_load_multiple_wallets(self):
        wallets = self.wallet.load_multiple_wallets(['jwk_file.json'])
        self.assertEqual(len(wallets), 1)
        self.assertIsInstance(wallets[0], Wallet)

    def test_wallet_set_custom_api_endpoint(self):
        old_url = self.wallet.api_url
        self.wallet.set_custom_api_endpoint("new_api_url")
        self.assertEqual(self.wallet.api_url, "new_api_url")
        self.wallet.api_url = old_url  # Reset to original

    def test_wallet_enable_advanced_logging(self):
        self.wallet.enable_advanced_logging()
        self.assertTrue(logging.getLogger(__name__).getEffectiveLevel() == logging.DEBUG)

    # Transaction tests
    def test_transaction_init(self):
        self.assertIsNotNone(self.transaction.id)
        self.assertIsNotNone(self.transaction.last_tx)
        self.assertEqual(self.transaction.data_size, len(self.test_data))
        self.assertEqual(self.transaction.data, base64url_encode(self.test_data.encode('utf-8')).decode())

    def test_transaction_from_serialized_transaction(self):
        serialized = self.transaction.to_dict()
        new_tx = Transaction(self.wallet, transaction=json.dumps(serialized))
        self.assertEqual(self.transaction.last_tx, new_tx.last_tx)

    def test_transaction_get_reward(self):
        reward = self.transaction.get_reward(len(self.test_data))
        self.assertIsNotNone(reward)

    def test_transaction_add_tag(self):
        self.transaction.add_tag("test", "tag")
        self.assertEqual(len(self.transaction.tags), 1)

    def test_transaction_encode_tags(self):
        self.transaction.add_tag("test", "tag")
        self.transaction.encode_tags()
        self.assertTrue(isinstance(self.transaction.tags[0], str))

    def test_transaction_sign(self):
        self.transaction.sign()
        self.assertIsNotNone(self.transaction.signature)
        self.assertIsNotNone(self.transaction.id)

    def test_transaction_send(self):
        # Note: This test might fail if you don't have enough balance or if network issues occur
        with self.assertRaises(ArweaveTransactionException):
            self.transaction.send()

    def test_transaction_get_status(self):
        # This assumes that a transaction ID exists
        with self.assertRaises(ArweaveTransactionException):
            self.transaction.get_status()

    def test_transaction_get_transaction(self):
        # This test might fail if no transaction with this ID exists
        with self.assertRaises(ArweaveTransactionException):
            self.transaction.get_transaction()

    def test_transaction_get_price(self):
        price = self.transaction.get_price()
        self.assertIsNotNone(price)

    def test_transaction_get_data(self):
        # This test will fail unless there's actual data associated with a transaction ID
        with self.assertRaises(ArweaveTransactionException):
            self.transaction.get_data()

    def test_transaction_load_json(self):
        json_str = json.dumps(self.transaction.to_dict())
        self.transaction.load_json(json_str)
        self.assertEqual(self.transaction.owner, self.wallet.owner)

    def test_transaction_prepare_chunks(self):
        with TemporaryFile() as tf:
            tf.write(self.test_data.encode('utf-8'))
            tf.seek(0)
            tx = Transaction(self.wallet, file_handler=tf, file_path='temp.txt')
            tx.prepare_chunks()
            self.assertIsNotNone(tx.chunks)

    def test_transaction_get_chunk(self):
        with TemporaryFile() as tf:
            tf.write(self.test_data.encode('utf-8'))
            tf.seek(0)
            tx = Transaction(self.wallet, file_handler=tf, file_path='temp.txt')
            tx.prepare_chunks()
            chunk = tx.get_chunk(0)
            self.assertIsNotNone(chunk['chunk'])

    def test_estimate_transaction_fee(self):
        # Assuming the method is bound to Transaction instance
        fee = self.transaction.estimate_transaction_fee()
        self.assertIsNotNone(fee)

    def test_add_metadata(self):
        self.transaction.add_metadata({"test": "metadata"})
        self.assertEqual(self.transaction.metadata, {"test": "metadata"})

    def test_schedule_transaction(self):
        self.transaction.schedule_transaction(1638316800)  # Example Unix timestamp
        self.assertEqual(self.transaction.scheduled_time, 1638316800)

    # Utils tests
    def test_utils_listen_for_transaction(self):
        # This test would need an actual transaction ID that's being confirmed
        with self.assertRaises(ArweaveTransactionException):
            Utils.listen_for_transaction("invalid_transaction_id")

    def test_utils_send_batch_transactions(self):
        # This test requires at least two transactions for a batch
        tx1 = Transaction(self.wallet, data="batch test 1")
        tx2 = Transaction(self.wallet, data="batch test 2")
        results = Utils.send_batch_transactions(self.wallet, [tx1, tx2])
        # Check if results are lists of transaction IDs or if exceptions were raised
        self.assertEqual(len(results), 2)

    def test_utils_compress_and_store_data(self):
        compressed = Utils.compress_and_store_data(self.test_data)
        self.assertIsNotNone(compressed)
        self.assertNotEqual(compressed, self.test_data)

    def test_utils_encrypt_and_store(self):
        key = Fernet.generate_key()
        encrypted = Utils.encrypt_and_store(self.test_data, key)
        self.assertIsNotNone(encrypted)
        self.assertNotEqual(encrypted, self.test_data.encode())

    def test_utils_sync_with_blockchain(self):
        status = Utils.sync_with_blockchain()
        self.assertIsInstance(status, dict)
        self.assertIn('height', status)  # Assuming 'height' is a key in network status

if __name__ == '__main__':
    unittest.main()