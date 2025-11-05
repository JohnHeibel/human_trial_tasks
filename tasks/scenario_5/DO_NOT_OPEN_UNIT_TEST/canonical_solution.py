from typing import Dict, List, Optional, Any


class UserProfileManager:
    """Manages user profiles with validation and search capabilities."""

    def __init__(self):
        """Initialize the user profile manager."""
        self.profiles: Dict[str, Dict[str, Any]] = {}

    def validate_username(self, username: str) -> bool:
        """
        Validate username format.

        Args:
            username: Username to validate

        Returns:
            True if valid, False otherwise
        """
        if not username or len(username) < 3 or len(username) > 20:
            return False

        return username.isalnum()

    def validate_email(self, email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email to validate

        Returns:
            True if valid, False otherwise
        """
        if not email or '@' not in email:
            return False

        parts = email.split('@')
        if len(parts) != 2:
            return False

        local, domain = parts
        if not local or not domain or '.' not in domain:
            return False

        return True

    def validate_age(self, age: int) -> bool:
        """
        Validate age is within acceptable range.

        Args:
            age: Age to validate

        Returns:
            True if valid, False otherwise
        """
        return isinstance(age, int) and 13 <= age <= 120

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
        # Validate inputs
        if not self.validate_username(username):
            return False

        if not self.validate_email(email):
            return False

        if not self.validate_age(age):
            return False

        # Check if user already exists (case-insensitive)
        username_lower = username.lower()
        if username_lower in self.profiles:
            return False

        # Create profile
        self.profiles[username_lower] = {
            'username': username,
            'email': email,
            'age': age,
            'bio': bio,
            'location': location
        }

        return True

    def get_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user profile.

        Args:
            username: Username to lookup (case-insensitive)

        Returns:
            Profile dictionary or None if not found
        """
        return self.profiles.get(username.lower())

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
        username_lower = username.lower()

        if username_lower not in self.profiles:
            return False

        # Validate new values if provided
        if email is not None:
            if not self.validate_email(email):
                return False
            self.profiles[username_lower]['email'] = email

        if age is not None:
            if not self.validate_age(age):
                return False
            self.profiles[username_lower]['age'] = age

        if bio is not None:
            self.profiles[username_lower]['bio'] = bio

        if location is not None:
            self.profiles[username_lower]['location'] = location

        return True

    def generate_summary(self, username: str) -> Optional[str]:
        """
        Generate a text summary of a user profile.

        Args:
            username: Username to generate summary for

        Returns:
            Summary string or None if user doesn't exist
        """
        profile = self.get_profile(username)

        if not profile:
            return None

        bio = profile['bio'] if profile['bio'] else "No bio"

        return f"{profile['username']} ({profile['age']}): {profile['email']} - {bio}"

    def search_by_age(self, min_age: int) -> List[str]:
        """
        Find all users at or above a minimum age.

        Args:
            min_age: Minimum age threshold

        Returns:
            List of usernames matching criteria
        """
        results = []

        for username, profile in self.profiles.items():
            if profile['age'] >= min_age:
                results.append(profile['username'])

        return sorted(results)

    def search_by_location(self, location: str) -> List[str]:
        """
        Find all users in a location (case-insensitive partial match).

        Args:
            location: Location string to search for

        Returns:
            List of usernames matching criteria
        """
        results = []
        location_lower = location.lower()

        for username, profile in self.profiles.items():
            if location_lower in profile['location'].lower():
                results.append(profile['username'])

        return sorted(results)
