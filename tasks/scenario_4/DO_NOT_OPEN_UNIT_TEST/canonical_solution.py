from typing import Dict


class LoginAuthenticator:
    """Simple login authentication system."""

    def __init__(self):
        """Initialize the authenticator."""
        self.users: Dict[str, Dict[str, any]] = {}

    def validate_username(self, username: str) -> bool:
        """
        Validate username format.

        Args:
            username: Username to validate

        Returns:
            True if valid, False otherwise
        """
        if not username or len(username) < 4 or len(username) > 15:
            return False

        return username.isalnum()

    def validate_password(self, password: str) -> bool:
        """
        Validate password meets minimum requirements.

        Args:
            password: Password to validate

        Returns:
            True if valid, False otherwise
        """
        return len(password) >= 6

    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user.

        Args:
            username: Username (4-15 alphanumeric)
            password: Password (minimum 6 characters)

        Returns:
            True if registered successfully, False otherwise
        """
        # Validate inputs
        if not self.validate_username(username):
            return False

        if not self.validate_password(password):
            return False

        # Check if user already exists
        username_lower = username.lower()
        if username_lower in self.users:
            return False

        # Register user
        self.users[username_lower] = {
            'password': password,
            'failed_attempts': 0
        }

        return True

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a login attempt.

        Args:
            username: Username to authenticate
            password: Password to verify

        Returns:
            True if credentials are correct, False otherwise
        """
        username_lower = username.lower()

        # Check if user exists
        if username_lower not in self.users:
            return False

        user = self.users[username_lower]

        # Check password
        if user['password'] == password:
            # Successful login - reset failed attempts
            user['failed_attempts'] = 0
            return True
        else:
            # Failed login - increment counter
            user['failed_attempts'] += 1
            return False

    def get_failed_attempts(self, username: str) -> int:
        """
        Get number of failed login attempts for a user.

        Args:
            username: Username to check

        Returns:
            Number of failed attempts, or 0 if user doesn't exist
        """
        username_lower = username.lower()

        if username_lower not in self.users:
            return 0

        return self.users[username_lower]['failed_attempts']

    def user_exists(self, username: str) -> bool:
        """
        Check if a user is registered.

        Args:
            username: Username to check

        Returns:
            True if user exists, False otherwise
        """
        return username.lower() in self.users
