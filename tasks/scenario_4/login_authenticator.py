from typing import Dict


class LoginAuthenticator:
    """Simple login authentication system."""

    def __init__(self):
        """Initialize the authenticator."""
        # TODO: Initialize users dictionary
        pass

    def validate_username(self, username: str) -> bool:
        """
        Validate username format.

        Args:
            username: Username to validate

        Returns:
            True if valid, False otherwise
        """
        # TODO: Check length is 4-15 characters
        # TODO: Check is alphanumeric
        pass

    def validate_password(self, password: str) -> bool:
        """
        Validate password meets minimum requirements.

        Args:
            password: Password to validate

        Returns:
            True if valid, False otherwise
        """
        # TODO: Check length is at least 6 characters
        pass

    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user.

        Args:
            username: Username (4-15 alphanumeric)
            password: Password (minimum 6 characters)

        Returns:
            True if registered successfully, False otherwise
        """
        # TODO: Validate username and password
        # TODO: Check if user already exists (case-insensitive)
        # TODO: Store user with password and failed_attempts = 0
        # TODO: Return True if successful, False otherwise
        pass

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate a login attempt.

        Args:
            username: Username to authenticate
            password: Password to verify

        Returns:
            True if credentials are correct, False otherwise
        """
        # TODO: Check if user exists (case-insensitive)
        # TODO: If password matches, reset failed_attempts to 0 and return True
        # TODO: If password doesn't match, increment failed_attempts and return False
        pass

    def get_failed_attempts(self, username: str) -> int:
        """
        Get number of failed login attempts for a user.

        Args:
            username: Username to check

        Returns:
            Number of failed attempts, or 0 if user doesn't exist
        """
        # TODO: Return failed_attempts for user, or 0 if not found
        pass

    def user_exists(self, username: str) -> bool:
        """
        Check if a user is registered.

        Args:
            username: Username to check

        Returns:
            True if user exists, False otherwise
        """
        # TODO: Check if username exists in users dict (case-insensitive)
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
