from typing import Dict, List, Optional, Any


class UserProfileManager:
    """Manages user profiles with validation and search capabilities."""

    def __init__(self):
        """Initialize the user profile manager."""
        # TODO: Initialize profiles dictionary
        pass

    def validate_username(self, username: str) -> bool:
        """
        Validate username format.

        Args:
            username: Username to validate

        Returns:
            True if valid, False otherwise
        """
        # TODO: Check length (3-20 characters)
        # TODO: Check alphanumeric only
        pass

    def validate_email(self, email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email to validate

        Returns:
            True if valid, False otherwise
        """
        # TODO: Check contains @
        # TODO: Split on @ and verify 2 parts
        # TODO: Check domain has . with content
        pass

    def validate_age(self, age: int) -> bool:
        """
        Validate age is within acceptable range.

        Args:
            age: Age to validate

        Returns:
            True if valid, False otherwise
        """
        # TODO: Check is integer
        # TODO: Check 13 <= age <= 120
        pass

    def create_profile(self, username: str, email: str, age: int,
                      bio: str = "", location: str = "") -> bool:
        """
        Create a new user profile.

        Args:
            username: Unique username (3-20 alphanumeric)
            email: User email address
            age: User age (13-120)
            bio: Optional biography
            location: Optional location

        Returns:
            True if created successfully, False if validation fails or user exists
        """
        # TODO: Validate username, email, age
        # TODO: Check if username already exists (case-insensitive)
        # TODO: Store profile with lowercase username as key
        # TODO: Return True if successful, False otherwise
        pass

    def get_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user profile.

        Args:
            username: Username to lookup (case-insensitive)

        Returns:
            Profile dictionary or None if not found
        """
        # TODO: Return profile using lowercase username
        pass

    def update_profile(self, username: str, email: Optional[str] = None,
                      age: Optional[int] = None, bio: Optional[str] = None,
                      location: Optional[str] = None) -> bool:
        """
        Update an existing user profile.

        Args:
            username: Username of profile to update
            email: New email (optional)
            age: New age (optional)
            bio: New bio (optional)
            location: New location (optional)

        Returns:
            True if updated successfully, False if user doesn't exist or validation fails
        """
        # TODO: Check if user exists
        # TODO: Validate and update each provided field
        # TODO: Return True if successful, False otherwise
        pass

    def generate_summary(self, username: str) -> Optional[str]:
        """
        Generate a text summary of a user profile.

        Args:
            username: Username to generate summary for

        Returns:
            Summary string or None if user doesn't exist
        """
        # TODO: Get profile
        # TODO: Format as "{username} ({age}): {email} - {bio}"
        # TODO: Use "No bio" if bio is empty
        pass

    def search_by_age(self, min_age: int) -> List[str]:
        """
        Find all users at or above a minimum age.

        Args:
            min_age: Minimum age threshold

        Returns:
            List of usernames matching criteria
        """
        # TODO: Loop through profiles
        # TODO: Collect usernames where age >= min_age
        # TODO: Return sorted list
        pass

    def search_by_location(self, location: str) -> List[str]:
        """
        Find all users in a location (case-insensitive partial match).

        Args:
            location: Location string to search for

        Returns:
            List of usernames matching criteria
        """
        # TODO: Loop through profiles
        # TODO: Check if location (lowercase) is in profile location (lowercase)
        # TODO: Return sorted list of matches
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
