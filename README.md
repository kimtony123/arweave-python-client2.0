# arweave-python-client

This client allows you to integrate your Python apps with the Arweave network, enabling wallet operations, transactions, and data storage.

## Installing

To use the library, simply install it:

```bash
pip install arweave-python-client
```

## Using Your Wallet

Once installed, you can import the library and supply the wallet object with the path to your wallet JSON file:

```python
import arweave

wallet_file_path = "/some/folder/on/your/system"
wallet = arweave.Wallet(wallet_file_path)

balance = wallet.balance

last_transaction = wallet.get_last_transaction_id()
```

### Loading Your Wallet

If your wallet data is stored in a secret manager or anywhere other than a file, you can load it with the `from_data` class method:

```python
import arweave

wallet_data = # Load from cloud storage or wherever
wallet = arweave.Wallet.from_data(wallet_data)

balance = wallet.balance
```

## Transactions

### Sending Transactions

To send a transaction, open your wallet, create a transaction object, sign it, and then post the transaction:

```python
import arweave

wallet_file_path = "/some/folder/on/your/system"
wallet = arweave.Wallet(wallet_file_path)

transaction = arweave.Transaction(wallet, quantity=0.3, to='<some wallet address>')
transaction.sign()
transaction.send()
```

**Note**: Quantity is in AR and is automatically converted to Winston before sending.

### Uploading Large Files

Uploading large data files is possible even if the file exceeds your physical memory or the maximum transaction size (12MB):

```python
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader

wallet = Wallet(jwk_file)

with open("my_large_file.dat", "rb", buffering=0) as file_handler:
    tx = Transaction(wallet, file_handler=file_handler, file_path="/some/path/my_large_file.dat")
    tx.add_tag('Content-Type', 'application/dat')
    tx.sign()

    uploader = get_uploader(tx, file_handler)

    while not uploader.is_complete:
        uploader.upload_chunk()
        logger.info(f"{uploader.pct_complete}% complete, {uploader.uploaded_chunks}/{uploader.total_chunks}")
```

**Note**: Supply a file handle with `buffering=0` instead of reading all data at once.

### Checking Transaction Status

To check the status of a transaction after sending:

```python
status = transaction.get_status()
```

To check the status later, store the transaction ID and reload it:

```python
transaction = Transaction(wallet, id='some id you stored')
status = transaction.get_status()
```

### Storing Data

Arweave allows permanent data storage on the network. Supply the data as a string:

```python
wallet = Wallet(jwk_file)

with open('myfile.pdf', 'r') as mypdf:
    pdf_string_data = mypdf.read()

    transaction = Transaction(wallet, data=pdf_string_data)
    transaction.sign()
    transaction.send()
```

### Retrieving Transactions/Data

To get information about a transaction:

```python
tx = Transaction(wallet, id=<your tx id>)
tx.get_transaction()
```

To retrieve the data attached to the transaction:

```python
tx.get_data()
print(tx.data)
# Output: "some data"
```

### Sending to a Specific Node

You can specify a node by setting the `api_url` of the wallet or transaction object:

```python
wallet = Wallet(jwk_file)
wallet.api_url = 'specific node address'

# Or
transaction = Transaction(wallet, data=pdf_string_data)
transaction.api_url = 'specific node address'
```

### ArQL

Perform searches using the ArQL method:

```python
from arweave.arweave_lib import arql

wallet_file_path = "/some/folder/on/your/system"
wallet = arweave.Wallet(wallet_file_path)

transaction_ids = arql(
    wallet,
    {
        "op": "equals",
        "expr1": "from",
        "expr2": "Some owner address"
    })
```

Alternatively, use the helper method `arql_with_transaction_data()` to get all transaction IDs and data:

```python
import arweave

wallet_file_path = "/some/folder/on/your/system"
wallet = arweave.Wallet(wallet_file_path)

transactions = arweave.arql_with_transaction_data(
    wallet,
    {
        "op": "equals",
        "expr1": "from",
        "expr2": "Some owner address"
    })
```

## New Features and Enhancements

### 1. Batch Transactions

Create multiple transactions and send them in one batch to improve efficiency:

```python
def create_batch_transactions(wallet, transactions):
    # Implement batch transaction logic here
    pass
```

### 2. Enhanced Wallet Recovery Options

Provide multiple recovery methods, including mnemonic phrases:

```python
def recover_wallet_from_mnemonic(mnemonic):
    # Implement recovery logic here
    pass
```

### 3. Transaction Scheduling

Schedule transactions to execute at specific times:

```python
from datetime import datetime, timedelta
import time

def schedule_transaction(transaction, execute_at):
    while datetime.now() < execute_at:
        time.sleep(1)
    transaction.send()
```

### 4. Data Encryption for Secure Storage

Encrypt data before uploading to ensure privacy:

```python
from cryptography.fernet import Fernet

def encrypt_and_store(wallet, data):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())

    transaction = Transaction(wallet, data=encrypted_data)
    transaction.sign()
    transaction.send()
    return key  # Store key securely
```

### 5. Data Compression for Efficient Storage

Compress data before uploading to save storage space:

```python
import zlib

def compress_and_store_data(wallet, data):
    compressed_data = zlib.compress(data.encode())
    transaction = Transaction(wallet, data=compressed_data)
    transaction.add_tag('Content-Encoding', 'gzip')
    transaction.sign()
    transaction.send()
```

### 6. Support for Bundled Transactions

Bundle smaller transactions into one for efficiency:

```python
def create_bundled_transaction(wallet, transactions):
    # Combine multiple transactions into one
    pass
```

### 7. Real-Time Blockchain Sync

Synchronize wallet activity or track transactions in real-time:

```python
import time

def sync_with_blockchain(wallet, callback):
    while True:
        current_balance = wallet.balance
        callback(current_balance)
        time.sleep(10)  # Sync every 10 seconds
```

### 8. Advanced Logging and Debugging

Enable detailed logging to monitor transaction status, network calls, and errors:

```python
import logging

def enable_advanced_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
```

### 9. Custom API Endpoints

Allow setting custom API endpoints for different environments (e.g., development, testing, production):

```python
def set_custom_api_endpoint(wallet, endpoint):
    wallet.api_url = endpoint
```

### 10. Multi-Wallet Support

Enable managing multiple wallets simultaneously:

```python
def load_multiple_wallets(wallet_paths):
    wallets = [Wallet(path) for path in wallet_paths]
    return wallets
```

### 11. Enhanced Security Features

Add two-factor authentication (2FA) for transaction signing:

```python
def enable_2fa(wallet, token):
    # Validate the token and enable 2FA
    pass
```

### 12. Offline Transaction Signing

Allow users to sign transactions offline and upload them later:

```python
def sign_transaction_offline(wallet, transaction):
    transaction.sign()
    return transaction
```
