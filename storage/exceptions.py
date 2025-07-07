"""
Custom exceptions for the secure storage module.
"""

class StorageError(Exception):
    """Base exception for all storage-related errors."""
    pass

class EncryptionError(StorageError):
    """Raised when encryption fails."""
    pass

class DecryptionError(StorageError):
    """Raised when decryption fails or authentication fails."""
    pass

class StorageInitializationError(StorageError):
    """Raised when storage initialization fails."""
    pass

class StorageIOError(StorageError):
    """Raised when there's an I/O error during storage operations."""
    pass
