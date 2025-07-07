# Secure Storage Module

This module provides secure, encrypted storage for sensitive data in VaultGPT. It's designed to be used as a storage layer rather than a separate agent, following security best practices.

## Features

- **AES-256-GCM Encryption**: Strong encryption for data at rest
- **Secure Key Management**: Keys derived from environment variables
- **Data Integrity**: Authentication tags ensure data hasn't been tampered with
- **Simple API**: Easy-to-use methods for storing and retrieving encrypted data
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

1. Install the required dependencies:
   ```bash
   pip install cryptography
   ```

2. Set up your environment variable:
   ```bash
   # On Linux/macOS
   export VAULTGPT_ENCRYPTION_KEY="your-very-secure-key-here"
   
   # On Windows
   set VAULTGPT_ENCRYPTION_KEY=your-very-secure-key-here
   ```

## Usage

### Basic Usage

```python
from storage import SecureStorage

# Initialize the secure storage
storage = SecureStorage()

# Encrypt and store data
encrypted = storage.encrypt_data({
    'account_number': '1234567890',
    'balance': 1000.50,
    'transactions': ['deposit', 'withdrawal']
})

# Store the encrypted data (you would typically save this to a database)
# ...

# Later, decrypt the data
decrypted = storage.decrypt_data(encrypted)
print(decrypted)  # Original data
```

### File Storage

```python
# Store encrypted data to a file
storage.store_encrypted(
    {'sensitive': 'data'},
    'path/to/secure/file.dat'
)

# Load and decrypt data from a file
data = storage.load_encrypted('path/to/secure/file.dat')
```

## Security Considerations

1. **Key Management**:
   - Never hardcode encryption keys in your source code
   - Use environment variables or a secure key management system
   - Rotate keys periodically

2. **Error Handling**:
   - Always handle encryption/decryption errors gracefully
   - Log errors without exposing sensitive information

3. **Performance**:
   - Encryption/decryption is CPU-intensive; batch operations when possible
   - Consider caching decrypted data in memory for frequently accessed information

## Best Practices

1. **Environment Variables**:
   - Use a strong, random key (at least 32 bytes)
   - Store the key securely (e.g., in a .env file not committed to version control)

2. **Data Organization**:
   - Store different types of data in separate encrypted files
   - Use meaningful file names that don't reveal sensitive information

3. **Backup**:
   - Regularly back up encrypted data
   - Test restoration procedures

## API Reference

### `SecureStorage`

#### `__init__(self, key_env_var: str = 'VAULTGPT_ENCRYPTION_KEY')`
Initialize the secure storage.

- `key_env_var`: Name of the environment variable containing the encryption key

#### `encrypt_data(self, data: Union[Dict, str, bytes]) -> Dict[str, str]`
Encrypt the provided data.

- `data`: Data to encrypt (dict, str, or bytes)
- Returns: Dictionary containing encrypted data and metadata
- Raises: `EncryptionError` if encryption fails

#### `decrypt_data(self, encrypted_data: Dict[str, str]) -> Union[Dict, str, bytes]`
Decrypt the provided encrypted data.

- `encrypted_data`: Dictionary containing 'ciphertext', 'salt', and 'nonce'
- Returns: Decrypted data (original format)
- Raises: `DecryptionError` if decryption fails

#### `store_encrypted(self, data: Any, storage_path: str) -> None`
Store encrypted data to a file.

- `data`: Data to encrypt and store
- `storage_path`: Path to store the encrypted data
- Raises: `StorageError` if storage operation fails

#### `load_encrypted(self, storage_path: str) -> Any`
Load and decrypt data from a file.

- `storage_path`: Path to the encrypted data file
- Returns: Decrypted data
- Raises: `StorageError` if storage operation fails

## Example: Integrating with VaultGPT

```python
# In your agent implementation
from storage import SecureStorage

class FinancialAgent:
    def __init__(self):
        self.storage = SecureStorage()
        
    def store_financial_data(self, user_id: str, data: dict):
        """Store encrypted financial data for a user."""
        storage_path = f"data/users/{user_id}/financial.dat"
        self.storage.store_encrypted(data, storage_path)
        
    def get_financial_data(self, user_id: str) -> dict:
        """Retrieve and decrypt financial data for a user."""
        storage_path = f"data/users/{user_id}/financial.dat"
        return self.storage.load_encrypted(storage_path)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
