import unittest
from user_profile_manager import UserProfileManager


class TestUserProfileManager(unittest.TestCase):
    """Test suite for user profile manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = UserProfileManager()

    # Validation tests

    def test_validate_username_valid(self):
        """Test valid usernames."""
        self.assertTrue(self.manager.validate_username("john123"))
        self.assertTrue(self.manager.validate_username("alice"))
        self.assertTrue(self.manager.validate_username("user2024"))

    def test_validate_username_invalid(self):
        """Test invalid usernames."""
        self.assertFalse(self.manager.validate_username("ab"))  # Too short
        self.assertFalse(self.manager.validate_username("a" * 21))  # Too long
        self.assertFalse(self.manager.validate_username("user@123"))  # Special char
        self.assertFalse(self.manager.validate_username(""))  # Empty

    def test_validate_email_valid(self):
        """Test valid emails."""
        self.assertTrue(self.manager.validate_email("user@example.com"))
        self.assertTrue(self.manager.validate_email("test@test.org"))

    def test_validate_email_invalid(self):
        """Test invalid emails."""
        self.assertFalse(self.manager.validate_email("notanemail"))
        self.assertFalse(self.manager.validate_email("@example.com"))
        self.assertFalse(self.manager.validate_email("user@"))
        self.assertFalse(self.manager.validate_email("user@domain"))  # No .

    def test_validate_age_valid(self):
        """Test valid ages."""
        self.assertTrue(self.manager.validate_age(13))
        self.assertTrue(self.manager.validate_age(25))
        self.assertTrue(self.manager.validate_age(120))

    def test_validate_age_invalid(self):
        """Test invalid ages."""
        self.assertFalse(self.manager.validate_age(12))  # Too young
        self.assertFalse(self.manager.validate_age(121))  # Too old
        self.assertFalse(self.manager.validate_age(-5))

    # Profile creation tests

    def test_create_profile_success(self):
        """Test successful profile creation."""
        result = self.manager.create_profile("alice", "alice@example.com", 25)
        self.assertTrue(result)

    def test_create_profile_with_optional_fields(self):
        """Test profile creation with bio and location."""
        result = self.manager.create_profile(
            "bob", "bob@example.com", 30,
            bio="Software developer", location="San Francisco"
        )
        self.assertTrue(result)

        profile = self.manager.get_profile("bob")
        self.assertEqual(profile['bio'], "Software developer")
        self.assertEqual(profile['location'], "San Francisco")

    def test_create_profile_invalid_username(self):
        """Test that invalid username fails."""
        result = self.manager.create_profile("ab", "test@example.com", 25)
        self.assertFalse(result)

    def test_create_profile_invalid_email(self):
        """Test that invalid email fails."""
        result = self.manager.create_profile("alice", "notanemail", 25)
        self.assertFalse(result)

    def test_create_profile_invalid_age(self):
        """Test that invalid age fails."""
        result = self.manager.create_profile("alice", "alice@example.com", 10)
        self.assertFalse(result)

    def test_create_profile_duplicate(self):
        """Test that duplicate username fails."""
        self.manager.create_profile("charlie", "charlie@example.com", 25)
        result = self.manager.create_profile("charlie", "other@example.com", 30)
        self.assertFalse(result)

    def test_create_profile_case_insensitive(self):
        """Test that usernames are case-insensitive."""
        self.manager.create_profile("Dave", "dave@example.com", 25)
        result = self.manager.create_profile("dave", "other@example.com", 30)
        self.assertFalse(result)

    # Profile retrieval tests

    def test_get_profile_exists(self):
        """Test retrieving existing profile."""
        self.manager.create_profile("eve", "eve@example.com", 28, bio="Tester")

        profile = self.manager.get_profile("eve")
        self.assertIsNotNone(profile)
        self.assertEqual(profile['username'], "eve")
        self.assertEqual(profile['email'], "eve@example.com")
        self.assertEqual(profile['age'], 28)
        self.assertEqual(profile['bio'], "Tester")

    def test_get_profile_not_exists(self):
        """Test retrieving non-existent profile."""
        profile = self.manager.get_profile("nobody")
        self.assertIsNone(profile)

    def test_get_profile_case_insensitive(self):
        """Test profile retrieval is case-insensitive."""
        self.manager.create_profile("Frank", "frank@example.com", 35)

        profile = self.manager.get_profile("frank")
        self.assertIsNotNone(profile)
        self.assertEqual(profile['username'], "Frank")

    # Profile update tests

    def test_update_profile_email(self):
        """Test updating email."""
        self.manager.create_profile("grace", "grace@example.com", 30)

        result = self.manager.update_profile("grace", email="newemail@example.com")
        self.assertTrue(result)

        profile = self.manager.get_profile("grace")
        self.assertEqual(profile['email'], "newemail@example.com")

    def test_update_profile_age(self):
        """Test updating age."""
        self.manager.create_profile("henry", "henry@example.com", 25)

        result = self.manager.update_profile("henry", age=26)
        self.assertTrue(result)

        profile = self.manager.get_profile("henry")
        self.assertEqual(profile['age'], 26)

    def test_update_profile_bio_location(self):
        """Test updating bio and location."""
        self.manager.create_profile("iris", "iris@example.com", 27)

        result = self.manager.update_profile("iris", bio="Designer", location="NYC")
        self.assertTrue(result)

        profile = self.manager.get_profile("iris")
        self.assertEqual(profile['bio'], "Designer")
        self.assertEqual(profile['location'], "NYC")

    def test_update_profile_not_exists(self):
        """Test updating non-existent profile fails."""
        result = self.manager.update_profile("nobody", email="test@example.com")
        self.assertFalse(result)

    def test_update_profile_invalid_email(self):
        """Test updating with invalid email fails."""
        self.manager.create_profile("jack", "jack@example.com", 30)

        result = self.manager.update_profile("jack", email="invalidemail")
        self.assertFalse(result)

    def test_update_profile_invalid_age(self):
        """Test updating with invalid age fails."""
        self.manager.create_profile("kate", "kate@example.com", 30)

        result = self.manager.update_profile("kate", age=10)
        self.assertFalse(result)

    # Summary generation tests

    def test_generate_summary_with_bio(self):
        """Test summary generation with bio."""
        self.manager.create_profile("leo", "leo@example.com", 32, bio="Engineer")

        summary = self.manager.generate_summary("leo")
        self.assertEqual(summary, "leo (32): leo@example.com - Engineer")

    def test_generate_summary_without_bio(self):
        """Test summary generation without bio."""
        self.manager.create_profile("mia", "mia@example.com", 24)

        summary = self.manager.generate_summary("mia")
        self.assertEqual(summary, "mia (24): mia@example.com - No bio")

    def test_generate_summary_not_exists(self):
        """Test summary for non-existent user."""
        summary = self.manager.generate_summary("nobody")
        self.assertIsNone(summary)

    # Search tests

    def test_search_by_age(self):
        """Test searching users by minimum age."""
        self.manager.create_profile("user1", "u1@example.com", 20)
        self.manager.create_profile("user2", "u2@example.com", 30)
        self.manager.create_profile("user3", "u3@example.com", 40)

        results = self.manager.search_by_age(25)
        self.assertEqual(len(results), 2)
        self.assertIn("user2", results)
        self.assertIn("user3", results)

    def test_search_by_age_no_matches(self):
        """Test age search with no matches."""
        self.manager.create_profile("young", "young@example.com", 18)

        results = self.manager.search_by_age(25)
        self.assertEqual(results, [])

    def test_search_by_location(self):
        """Test searching users by location."""
        self.manager.create_profile("user1", "u1@example.com", 25, location="New York")
        self.manager.create_profile("user2", "u2@example.com", 30, location="San Francisco")
        self.manager.create_profile("user3", "u3@example.com", 35, location="New Jersey")

        results = self.manager.search_by_location("New")
        self.assertEqual(len(results), 2)
        self.assertIn("user1", results)
        self.assertIn("user3", results)

    def test_search_by_location_case_insensitive(self):
        """Test location search is case-insensitive."""
        self.manager.create_profile("user1", "u1@example.com", 25, location="Paris")

        results = self.manager.search_by_location("paris")
        self.assertEqual(len(results), 1)
        self.assertIn("user1", results)

    def test_search_by_location_partial_match(self):
        """Test location search with partial match."""
        self.manager.create_profile("user1", "u1@example.com", 25, location="San Francisco")

        results = self.manager.search_by_location("Francisco")
        self.assertEqual(len(results), 1)


if __name__ == '__main__':
    unittest.main()
