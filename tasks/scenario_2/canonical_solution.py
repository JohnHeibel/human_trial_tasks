class PasswordStrengthChecker:
    """Checks password strength based on length and character diversity."""

    def __init__(self):
        """Initialize the password strength checker."""
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

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
        return {
            'has_lowercase': any(c.islower() for c in password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(c in self.special_chars for c in password)
        }

    def count_character_types(self, password: str) -> int:
        """
        Count how many different character types are in the password.

        Args:
            password: The password string to analyze

        Returns:
            Integer count of character types present (0-4)
        """
        char_types = self.check_character_types(password)
        return sum(char_types.values())

    def check_strength(self, password: str) -> str:
        """
        Evaluate password strength and return a rating.

        Args:
            password: The password string to evaluate

        Returns:
            One of: "weak", "medium", "strong"
        """
        # Empty password is weak
        if not password:
            return "weak"

        length = len(password)
        type_count = self.count_character_types(password)

        # Weak: Less than 8 characters OR missing 3+ character types
        if length < 8 or type_count <= 1:
            return "weak"

        # Strong: 12+ characters with at least 3 character types
        if length >= 12 and type_count >= 3:
            return "strong"

        # Medium: Everything else
        return "medium"
