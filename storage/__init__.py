"""
Secure Storage Module for VaultGPT

This module provides encrypted storage capabilities for sensitive data
using AES-256-GCM encryption. The encryption keys are managed securely
using environment variables and a key derivation function.
"""
from .secure_storage import SecureStorage
from .exceptions import EncryptionError, DecryptionError, StorageError

__all__ = ['SecureStorage', 'EncryptionError', 'DecryptionError', 'StorageError']
