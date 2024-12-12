# arweave-python-client2.0

This client allows you to integrate your Python apps with the Arweave network, enabling wallet operations, transactions, and data storage.

## Installing

The library can only be installed and used locally. To run it locally;

```bash
pip install .
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

### 1. Transaction Listener.

A function to listen for transaction confirmations or specific events.

```python
def listen_for_transaction(wallet, tx_id, callback):
    while True:
        status = Transaction(wallet, id=tx_id).get_status()
        if status == 'confirmed':
            callback(tx_id)
            break


```

### 2. Batch Transactions

Enable sending multiple transactions in a single function call to reduce overhead for bulk operations.

```python
def send_batch_transactions(wallet, transactions):
    for tx in transactions:
        tx.sign()
        tx.send()
```

### 3. Transaction Fee Estimator.

Provide an estimated transaction fee based on the size of data being uploaded.

```python
def estimate_transaction_fee(data_size):
    # Estimate fee based on Arweave's pricing model
    return data_size * fee_per_byte
```

### 3. Metadata Management for Files.

Add the ability to attach and retrieve metadata for uploaded files.

```python
def add_metadata(transaction, metadata):
    for key, value in metadata.items():
        transaction.add_tag(key, value)
```

### 4. Data Compression for Efficient Storage.

Compress data before uploading to save storage space and reduce costs.

```python
import zlib
def compress_and_store_data(wallet, data):
    compressed_data = zlib.compress(data.encode())
    transaction = arweave.Transaction(wallet, data=compressed_data)
    transaction.add_tag('Content-Encoding', 'gzip')
    transaction.sign()
    transaction.send()
```

### 5. Real-Time Blockchain Sync.

Synchronize wallet activity or track transactions in real-time.

```python
def sync_with_blockchain(wallet, callback):
    while True:
        current_balance = wallet.balance
        callback(current_balance)
        time.sleep(10)  # Sync every 10 seconds
```

### 6. Transaction Scheduling.

Schedule transactions to execute at specific times:

```python
from datetime import datetime, timedelta
import time

def schedule_transaction(transaction, execute_at):
    while datetime.now() < execute_at:
        time.sleep(1)
    transaction.send()
```

### 7. Data Encryption for Secure Storage.

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

### 8. Custom API Endpoints.

Allow setting custom API endpoints for different environments (e.g., development, testing, production):

```python
def set_custom_api_endpoint(wallet, endpoint):
    wallet.api_url = endpoint
```

### 9. Multi-Wallet Support.

Enable managing multiple wallets simultaneously:

```python
def set_custom_api_endpoint(wallet, endpoint):
    wallet.api_url = endpoint
```

### 10. Multi-Wallet Support

Enable managing multiple wallets simultaneously.

```python
def load_multiple_wallets(wallet_paths):
    wallets = [Wallet(path) for path in wallet_paths]
    return wallets
```

### 11. Advanced Logging and Debugging.

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
