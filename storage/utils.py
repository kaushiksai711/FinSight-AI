"""
Utility functions for the secure storage module.
"""
import os
import json
from typing import Any, Dict, Optional, Union
from pathlib import Path
from .exceptions import StorageError

def ensure_directory(path: str) -> None:
    """Ensure that the directory exists, create it if it doesn't.
    
    Args:
        path: Directory path to check/create
        
    Raises:
        StorageError: If directory creation fails
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise StorageError(f"Failed to create directory {path}: {str(e)}")

def is_valid_path(path: str) -> bool:
    """Check if a path is valid and writable.
    
    Args:
        path: Path to check
        
    Returns:
        bool: True if path is valid and writable, False otherwise
    """
    try:
        Path(path).touch()
        os.remove(path)
        return True
    except (OSError, IOError):
        return False

def serialize_data(data: Any) -> str:
    """Serialize data to JSON string.
    
    Args:
        data: Data to serialize
        
    Returns:
        str: JSON string representation of the data
        
    Raises:
        StorageError: If serialization fails
    """
    try:
        return json.dumps(data, default=str)
    except (TypeError, ValueError) as e:
        raise StorageError(f"Failed to serialize data: {str(e)}")

def deserialize_data(data_str: str) -> Any:
    """Deserialize data from JSON string.
    
    Args:
        data_str: JSON string to deserialize
        
    Returns:
        Deserialized data
        
    Raises:
        StorageError: If deserialization fails
    """
    try:
        return json.loads(data_str)
    except json.JSONDecodeError as e:
        raise StorageError(f"Failed to deserialize data: {str(e)}")

def get_app_data_dir(app_name: str = "VaultGPT") -> str:
    """Get the application data directory for the current platform.
    
    Args:
        app_name: Name of the application
        
    Returns:
        str: Path to the application data directory
    """
    if os.name == 'nt':  # Windows
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
        return os.path.join(base, app_name)
    else:  # macOS and Linux
        return os.path.join(os.path.expanduser('~'), f".{app_name.lower()}")

def get_secure_temp_dir() -> str:
    """Get a secure temporary directory for sensitive operations.
    
    Returns:
        str: Path to a secure temporary directory
    """
    import tempfile
    temp_dir = os.path.join(tempfile.gettempdir(), 'vaultgpt_secure_temp')
    os.makedirs(temp_dir, mode=0o700, exist_ok=True)
    return temp_dir
