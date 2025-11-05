class PasswordStrengthChecker:
    """Checks password strength based on length and character diversity."""

    def __init__(self):
        """Initialize the password strength checker."""
        # TODO: Define what counts as special characters
        # Hint: Store a string of special characters like "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pass

    def check_character_types(self, password: str) -> dict:
        """
        Check which character types are present in the password.

        Args:
            password: The password string to analyze

        Returns:
            Dictionary with boolean values for each character type:
            {
                'has_lowercase': bool,
                'has_uppercase': bool,
                'has_digit': bool,
                'has_special': bool
            }
        """
        # TODO: Check for each character type in the password
        # Hint: Use str.islower(), str.isupper(), str.isdigit()
        # Hint: For special chars, check if character is in your special_chars string
        # Hint: Use any() with a generator expression to check if at least one char matches
        pass

    def count_character_types(self, password: str) -> int:
        """
        Count how many different character types are in the password.

        Args:
            password: The password string to analyze

        Returns:
            Integer count of character types present (0-4)
        """
        # TODO: Use check_character_types() and count how many are True
        # Hint: sum() works on boolean values (True=1, False=0)
        pass

    def check_strength(self, password: str) -> str:
        """
        Evaluate password strength and return a rating.

        Args:
            password: The password string to evaluate

        Returns:
            One of: "weak", "medium", "strong"
        """
        # TODO: Implement password strength logic
        # 1. Handle empty password (return "weak")
        # 2. Get password length and character type count
        # 3. Apply strength rules:
        #    - Weak: length < 8 OR type_count <= 1
        #    - Strong: length >= 12 AND type_count >= 3
        #    - Medium: everything else
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
