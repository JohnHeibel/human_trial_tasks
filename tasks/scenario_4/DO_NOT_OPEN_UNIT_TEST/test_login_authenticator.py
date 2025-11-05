import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from login_authenticator import LoginAuthenticator


class TestLoginAuthenticator(unittest.TestCase):
    """Test suite for login authenticator."""

    def setUp(self):
        """Set up test fixtures."""
        self.auth = LoginAuthenticator()

    # Validation tests

    def test_validate_username_valid(self):
        """Test valid usernames."""
        self.assertTrue(self.auth.validate_username("user123"))
        self.assertTrue(self.auth.validate_username("alice"))
        self.assertTrue(self.auth.validate_username("test2024"))

    def test_validate_username_invalid(self):
        """Test invalid usernames."""
        self.assertFalse(self.auth.validate_username("abc"))  # Too short
        self.assertFalse(self.auth.validate_username("a" * 16))  # Too long
        self.assertFalse(self.auth.validate_username("user@123"))  # Special char

    def test_validate_password_valid(self):
        """Test valid passwords."""
        self.assertTrue(self.auth.validate_password("password"))
        self.assertTrue(self.auth.validate_password("123456"))
        self.assertTrue(self.auth.validate_password("pass!@#123"))

    def test_validate_password_invalid(self):
        """Test invalid passwords."""
        self.assertFalse(self.auth.validate_password("short"))  # Too short
        self.assertFalse(self.auth.validate_password("12345"))  # Too short

    # Registration tests

    def test_register_user_success(self):
        """Test successful user registration."""
        result = self.auth.register_user("alice", "password123")
        self.assertTrue(result)

    def test_register_user_invalid_username(self):
        """Test registration fails with invalid username."""
        result = self.auth.register_user("abc", "password123")
        self.assertFalse(result)

    def test_register_user_invalid_password(self):
        """Test registration fails with invalid password."""
        result = self.auth.register_user("alice", "short")
        self.assertFalse(result)

    def test_register_user_duplicate(self):
        """Test registration fails for duplicate username."""
        self.auth.register_user("bob", "password123")
        result = self.auth.register_user("bob", "differentpass")
        self.assertFalse(result)

    def test_register_user_case_insensitive(self):
        """Test registration is case-insensitive."""
        self.auth.register_user("Charlie", "password123")
        result = self.auth.register_user("charlie", "password456")
        self.assertFalse(result)

    # Login tests

    def test_login_success(self):
        """Test successful login."""
        self.auth.register_user("dave", "mypassword")
        result = self.auth.login("dave", "mypassword")
        self.assertTrue(result)

    def test_login_wrong_password(self):
        """Test login fails with wrong password."""
        self.auth.register_user("eve", "correct123")
        result = self.auth.login("eve", "wrong123")
        self.assertFalse(result)

    def test_login_nonexistent_user(self):
        """Test login fails for non-existent user."""
        result = self.auth.login("nobody", "password123")
        self.assertFalse(result)

    def test_login_case_insensitive_username(self):
        """Test login works with different case."""
        self.auth.register_user("Frank", "password123")
        result = self.auth.login("frank", "password123")
        self.assertTrue(result)

    # Failed attempts tracking

    def test_failed_attempts_increment(self):
        """Test failed attempts are counted."""
        self.auth.register_user("grace", "password123")

        self.auth.login("grace", "wrong1")
        self.assertEqual(self.auth.get_failed_attempts("grace"), 1)

        self.auth.login("grace", "wrong2")
        self.assertEqual(self.auth.get_failed_attempts("grace"), 2)

        self.auth.login("grace", "wrong3")
        self.assertEqual(self.auth.get_failed_attempts("grace"), 3)

    def test_failed_attempts_reset_on_success(self):
        """Test failed attempts reset after successful login."""
        self.auth.register_user("henry", "password123")

        self.auth.login("henry", "wrong")
        self.auth.login("henry", "wrong")
        self.assertEqual(self.auth.get_failed_attempts("henry"), 2)

        # Successful login should reset
        self.auth.login("henry", "password123")
        self.assertEqual(self.auth.get_failed_attempts("henry"), 0)

    def test_failed_attempts_nonexistent_user(self):
        """Test failed attempts returns 0 for non-existent user."""
        count = self.auth.get_failed_attempts("nobody")
        self.assertEqual(count, 0)

    # User existence tests

    def test_user_exists_true(self):
        """Test user_exists returns True for registered user."""
        self.auth.register_user("iris", "password123")
        self.assertTrue(self.auth.user_exists("iris"))

    def test_user_exists_false(self):
        """Test user_exists returns False for non-registered user."""
        self.assertFalse(self.auth.user_exists("nobody"))

    def test_user_exists_case_insensitive(self):
        """Test user_exists is case-insensitive."""
        self.auth.register_user("Jack", "password123")
        self.assertTrue(self.auth.user_exists("jack"))
        self.assertTrue(self.auth.user_exists("JACK"))


if __name__ == '__main__':
    unittest.main()
