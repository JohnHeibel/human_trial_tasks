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
        self.prefix = prefix
        self.keys: Dict[str, Dict[str, Any]] = {}

    def generate_key(self, metadata: Dict[str, Any]) -> str:
        """
        Generate a new API key with associated metadata.

        Args:
            metadata: Dictionary containing user information
                     (e.g., {'user_id': '123', 'email': 'user@example.com', 'permissions': ['read', 'write']})

        Returns:
            The generated API key string
        """
        # Generate cryptographically secure random hex string
        random_part = secrets.token_hex(16)  # 16 bytes = 32 hex characters

        # Combine prefix with random part
        api_key = f"{self.prefix}{random_part}"

        # Ensure uniqueness (very unlikely to collide, but check anyway)
        while api_key in self.keys:
            random_part = secrets.token_hex(16)
            api_key = f"{self.prefix}{random_part}"

        # Store key with metadata
        self.keys[api_key] = metadata.copy()

        return api_key

    def validate_key(self, api_key: str) -> bool:
        """
        Check if an API key is valid.

        Args:
            api_key: The API key string to validate

        Returns:
            True if key is valid (exists), False otherwise
        """
        return api_key in self.keys

    def get_metadata(self, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata associated with an API key.

        Args:
            api_key: The API key string

        Returns:
            Dictionary of metadata if key exists, None otherwise
        """
        return self.keys.get(api_key)

    def revoke_key(self, api_key: str) -> bool:
        """
        Revoke (delete) an API key.

        Args:
            api_key: The API key string to revoke

        Returns:
            True if key was revoked, False if key didn't exist
        """
        if api_key in self.keys:
            del self.keys[api_key]
            return True
        return False

    def list_user_keys(self, user_id: str) -> List[str]:
        """
        List all API keys associated with a specific user.

        Args:
            user_id: The user ID to search for

        Returns:
            List of API key strings belonging to this user
        """
        user_keys = []
        for api_key, metadata in self.keys.items():
            if metadata.get('user_id') == user_id:
                user_keys.append(api_key)
        return user_keys

    def get_all_keys(self) -> List[str]:
        """
        Get a list of all active API keys.

        Returns:
            List of all API key strings
        """
        return list(self.keys.keys())
