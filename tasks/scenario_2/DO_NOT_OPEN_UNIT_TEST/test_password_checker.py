import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from password_checker import PasswordStrengthChecker


class TestPasswordStrengthChecker(unittest.TestCase):
    """Test suite for password strength checker."""

    def setUp(self):
        """Set up test fixtures."""
        self.checker = PasswordStrengthChecker()

    def test_empty_password_is_weak(self):
        """Test that empty passwords are rated as weak."""
        self.assertEqual(self.checker.check_strength(""), "weak")

    def test_short_password_is_weak(self):
        """Test that passwords under 8 characters are weak."""
        short_passwords = ["abc", "Pass1!", "aB3$", "1234567"]
        for password in short_passwords:
            self.assertEqual(
                self.checker.check_strength(password),
                "weak",
                f"Password '{password}' should be weak"
            )

    def test_long_password_one_type_is_weak(self):
        """Test that even long passwords with only one character type are weak."""
        self.assertEqual(self.checker.check_strength("abcdefghijklmnop"), "weak")
        self.assertEqual(self.checker.check_strength("12345678901234"), "weak")

    def test_medium_password_basic(self):
        """Test basic medium strength passwords."""
        medium_passwords = [
            "password123",      # 11 chars, 2 types (lowercase, digits)
            "PASSWORD123",      # 11 chars, 2 types (uppercase, digits)
            "Password",         # 8 chars, 2 types (upper, lower)
            "pass1234word",     # 12 chars, 2 types (lower, digits)
        ]
        for password in medium_passwords:
            self.assertEqual(
                self.checker.check_strength(password),
                "medium",
                f"Password '{password}' should be medium"
            )

    def test_strong_password_basic(self):
        """Test basic strong passwords."""
        strong_passwords = [
            "Password123!",          # 12 chars, 4 types
            "MyP@ssw0rd2024",       # 14 chars, 4 types
            "Secure#Pass99",         # 13 chars, 4 types
            "abcDEF123!!!",          # 12 chars, 4 types
        ]
        for password in strong_passwords:
            self.assertEqual(
                self.checker.check_strength(password),
                "strong",
                f"Password '{password}' should be strong"
            )

    def test_character_type_detection_lowercase(self):
        """Test detection of lowercase letters."""
        result = self.checker.check_character_types("abc")
        self.assertTrue(result['has_lowercase'])
        self.assertFalse(result['has_uppercase'])
        self.assertFalse(result['has_digit'])
        self.assertFalse(result['has_special'])

    def test_character_type_detection_uppercase(self):
        """Test detection of uppercase letters."""
        result = self.checker.check_character_types("ABC")
        self.assertFalse(result['has_lowercase'])
        self.assertTrue(result['has_uppercase'])
        self.assertFalse(result['has_digit'])
        self.assertFalse(result['has_special'])

    def test_character_type_detection_digits(self):
        """Test detection of digits."""
        result = self.checker.check_character_types("12345")
        self.assertFalse(result['has_lowercase'])
        self.assertFalse(result['has_uppercase'])
        self.assertTrue(result['has_digit'])
        self.assertFalse(result['has_special'])

    def test_character_type_detection_special(self):
        """Test detection of special characters."""
        special_chars = "!@#$%^&*()"
        result = self.checker.check_character_types(special_chars)
        self.assertFalse(result['has_lowercase'])
        self.assertFalse(result['has_uppercase'])
        self.assertFalse(result['has_digit'])
        self.assertTrue(result['has_special'])

    def test_character_type_detection_mixed(self):
        """Test detection with mixed character types."""
        result = self.checker.check_character_types("Pass123!")
        self.assertTrue(result['has_lowercase'])
        self.assertTrue(result['has_uppercase'])
        self.assertTrue(result['has_digit'])
        self.assertTrue(result['has_special'])

    def test_count_character_types(self):
        """Test counting of character types."""
        test_cases = [
            ("", 0),
            ("abc", 1),
            ("Abc", 2),
            ("Abc1", 3),
            ("Abc1!", 4),
            ("aaa", 1),
            ("aA1!", 4),
        ]
        for password, expected_count in test_cases:
            self.assertEqual(
                self.checker.count_character_types(password),
                expected_count,
                f"Password '{password}' should have {expected_count} types"
            )

    def test_boundary_8_characters(self):
        """Test the 8-character boundary for weak/medium."""
        # 7 chars with 2 types - weak
        self.assertEqual(self.checker.check_strength("Pass123"), "weak")
        # 8 chars with 2 types - medium
        self.assertEqual(self.checker.check_strength("Pass1234"), "medium")

    def test_boundary_12_characters(self):
        """Test the 12-character boundary for medium/strong."""
        # 11 chars with 3 types - medium
        self.assertEqual(self.checker.check_strength("Password12!"), "medium")
        # 12 chars with 3 types - strong
        self.assertEqual(self.checker.check_strength("Password123!"), "strong")

    def test_strong_requires_three_types(self):
        """Test that strong passwords need at least 3 character types."""
        # 12+ chars but only 2 types - medium
        self.assertEqual(self.checker.check_strength("password12345"), "medium")
        self.assertEqual(self.checker.check_strength("PASSWORD12345"), "medium")

        # 12+ chars with 3 types - strong
        self.assertEqual(self.checker.check_strength("Password12345"), "strong")

    def test_various_special_characters(self):
        """Test that various special characters are recognized."""
        special_test_passwords = [
            "Pass123!word",   # exclamation
            "Pass123@word",   # at
            "Pass123#word",   # hash
            "Pass123$word",   # dollar
            "Pass123%word",   # percent
            "Pass123^word",   # caret
            "Pass123&word",   # ampersand
            "Pass123*word",   # asterisk
        ]
        for password in special_test_passwords:
            char_types = self.checker.check_character_types(password)
            self.assertTrue(
                char_types['has_special'],
                f"Password '{password}' should have special characters detected"
            )

    def test_only_special_characters(self):
        """Test password with only special characters."""
        # Even long special-only passwords are weak (only 1 type)
        self.assertEqual(self.checker.check_strength("!@#$%^&*()_+"), "weak")

    def test_realistic_weak_passwords(self):
        """Test realistic weak passwords."""
        weak_passwords = [
            "password",
            "123456",
            "qwerty",
            "abc123",
            "12345678",
        ]
        for password in weak_passwords:
            self.assertEqual(
                self.checker.check_strength(password),
                "weak",
                f"Common password '{password}' should be weak"
            )

        # Slightly more complex but still common patterns should only be medium
        self.assertEqual(self.checker.check_strength("password1"), "medium")

    def test_realistic_strong_passwords(self):
        """Test realistic strong passwords."""
        strong_passwords = [
            "MyDog&Cat2024!",
            "Tr0ub4dor&3Extended",
            "CorrectHorseBatteryStaple123!",
            "P@ssw0rd_Secure_2024",
        ]
        for password in strong_passwords:
            self.assertEqual(
                self.checker.check_strength(password),
                "strong",
                f"Password '{password}' should be strong"
            )


if __name__ == '__main__':
    unittest.main()
