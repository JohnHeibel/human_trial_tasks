import secrets
from typing import Dict, Any, List, Optional


class APIKeyManager:
    """Manages API key generation and validation."""

    def __init__(self, prefix: str = "sk_"):
        """
        Initialize the API key manager.

        Args:
            prefix: Prefix for generated keys (default: "sk_")
        """
        # TODO: Store the prefix
        # TODO: Initialize a dictionary to store keys and their metadata
        pass

    def generate_key(self, metadata: Dict[str, Any]) -> str:
        """
        Generate a new API key with associated metadata.

        Args:
            metadata: Dictionary containing user information
                     (e.g., {'user_id': '123', 'email': 'user@example.com', 'permissions': ['read', 'write']})

        Returns:
            The generated API key string
        """
        # TODO: Generate a cryptographically secure random hex string
        # Hint: Use secrets.token_hex(16) to get 32 hex characters
        # TODO: Combine prefix with the random part
        # TODO: Store the key with its metadata (make a copy of metadata dict)
        # TODO: Return the generated key
        pass

    def validate_key(self, api_key: str) -> bool:
        """
        Check if an API key is valid.

        Args:
            api_key: The API key string to validate

        Returns:
            True if key is valid (exists), False otherwise
        """
        # TODO: Check if the api_key exists in self.keys
        pass

    def get_metadata(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata associated with an API key.

        Args:
            api_key: The API key string

        Returns:
            Dictionary of metadata if key exists, None otherwise
        """
        # TODO: Return the metadata for this key, or None if not found
        # Hint: Use dict.get() method
        pass

    def revoke_key(self, api_key: str) -> bool:
        """
        Revoke (delete) an API key.

        Args:
            api_key: The API key string to revoke

        Returns:
            True if key was revoked, False if key didn't exist
        """
        # TODO: Check if key exists
        # TODO: If exists, delete it and return True
        # TODO: If doesn't exist, return False
        pass

    def list_user_keys(self, user_id: str) -> List[str]:
        """
        List all API keys associated with a specific user.

        Args:
            user_id: The user ID to search for

        Returns:
            List of API key strings belonging to this user
        """
        # TODO: Iterate through all keys and their metadata
        # TODO: Check if metadata contains 'user_id' that matches
        # TODO: Collect matching keys in a list and return
        pass

    def get_all_keys(self) -> List[str]:
        """
        Get a list of all active API keys.

        Returns:
            List of all API key strings
        """
        # TODO: Return a list of all keys
        # Hint: Convert dict.keys() to a list
        pass


if __name__ == '__main__':
    import unittest
    import sys
    import os

    # Add the test directory to path
    test_dir = os.path.join(os.path.dirname(__file__), 'DO_NOT_OPEN_UNIT_TEST')
    sys.path.insert(0, test_dir)

    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
