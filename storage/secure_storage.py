"""
Secure Storage Implementation

Provides encrypted storage using AES-256-GCM for data at rest.
Uses environment variables for key management and PBKDF2 for key derivation.
"""
import os
import json
import base64
import hashlib
import secrets
from typing import Any, Dict, Optional, Union
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureStorage:
    """Secure storage class that handles encryption/decryption of data."""
    
    # Constants
    SALT_LENGTH = 16
    NONCE_LENGTH = 12
    KEY_LENGTH = 32  # 256 bits for AES-256
    ITERATIONS = 100000
    
    def __init__(self, key_env_var: str = 'VAULTGPT_ENCRYPTION_KEY'):
        """Initialize the secure storage with encryption key from environment.
        
        Args:
            key_env_var: Environment variable name containing the encryption key
        """
        self.key_env_var = key_env_var
        self._validate_environment()
    
    def _validate_environment(self) -> None:
        """Validate that required environment variables are set."""
        if not os.getenv(self.key_env_var):
            raise EnvironmentError(
                f"Encryption key not found in environment variable: {self.key_env_var}"
            )
    
    def _derive_key(self, salt: bytes) -> bytes:
        """Derive a secure encryption key from the master key and salt.
        
        Args:
            salt: Random salt for key derivation
            
        Returns:
            Derived encryption key
        """
        master_key = os.environ[self.key_env_var].encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_LENGTH,
            salt=salt,
            iterations=self.ITERATIONS,
        )
        return kdf.derive(master_key)
    
    def encrypt_data(self, data: Union[Dict, str, bytes]) -> Dict[str, str]:
        """Encrypt the provided data.
        
        Args:
            data: Data to encrypt (dict, str, or bytes)
            
        Returns:
            Dictionary containing encrypted data and metadata
            
        Raises:
            EncryptionError: If encryption fails
        """
        try:
            # Convert data to bytes if it's a string
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, dict):
                data_bytes = json.dumps(data).encode('utf-8')
            else:
                data_bytes = data
            
            # Generate random salt and nonce
            salt = secrets.token_bytes(self.SALT_LENGTH)
            nonce = secrets.token_bytes(self.NONCE_LENGTH)
            
            # Derive key and initialize cipher
            key = self._derive_key(salt)
            aesgcm = AESGCM(key)
            
            # Encrypt the data
            encrypted_data = aesgcm.encrypt(
                nonce=nonce,
                data=data_bytes,
                associated_data=None
            )
            
            # Return as base64-encoded strings for easy storage
            return {
                'ciphertext': base64.b64encode(encrypted_data).decode('utf-8'),
                'salt': base64.b64encode(salt).decode('utf-8'),
                'nonce': base64.b64encode(nonce).decode('utf-8')
            }
            
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise EncryptionError(f"Failed to encrypt data: {str(e)}")
    
    def decrypt_data(self, encrypted_data: Dict[str, str]) -> Union[Dict, str, bytes]:
        """Decrypt the provided encrypted data.
        
        Args:
            encrypted_data: Dictionary containing 'ciphertext', 'salt', and 'nonce'
            
        Returns:
            Decrypted data (original format)
            
        Raises:
            DecryptionError: If decryption fails or authentication fails
        """
        try:
            # Decode base64 strings
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])
            salt = base64.b64decode(encrypted_data['salt'])
            nonce = base64.b64decode(encrypted_data['nonce'])
            
            # Derive key and initialize cipher
            key = self._derive_key(salt)
            aesgcm = AESGCM(key)
            
            # Decrypt the data
            decrypted_data = aesgcm.decrypt(
                nonce=nonce,
                data=ciphertext,
                associated_data=None
            )
            
            # Try to decode as JSON, otherwise return as bytes/string
            try:
                return json.loads(decoded:=decrypted_data.decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return decoded if 'decoded' in locals() else decrypted_data
                
        except InvalidTag as e:
            logger.error("Decryption failed: Authentication tag verification failed")
            raise DecryptionError("Authentication failed - data may have been tampered with")
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise DecryptionError(f"Failed to decrypt data: {str(e)}")

    def store_encrypted(self, data: Any, storage_path: str) -> None:
        """Store encrypted data to a file.
        
        Args:
            data: Data to encrypt and store
            storage_path: Path to store the encrypted data
            
        Raises:
            StorageError: If storage operation fails
        """
        try:
            encrypted = self.encrypt_data(data)
            with open(storage_path, 'w') as f:
                json.dump(encrypted, f)
        except Exception as e:
            raise StorageError(f"Failed to store encrypted data: {str(e)}")
    
    def load_encrypted(self, storage_path: str) -> Any:
        """Load and decrypt data from a file.
        
        Args:
            storage_path: Path to the encrypted data file
            
        Returns:
            Decrypted data
            
        Raises:
            StorageError: If storage operation fails
        """
        try:
            with open(storage_path, 'r') as f:
                encrypted = json.load(f)
            return self.decrypt_data(encrypted)
        except Exception as e:
            raise StorageError(f"Failed to load encrypted data: {str(e)}")
