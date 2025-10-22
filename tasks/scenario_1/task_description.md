# Task 1: Password Strength Checker

## Task Description

Implement a password strength checker that analyzes passwords and returns a strength rating based on various criteria. This is a fundamental security component that helps users create stronger passwords.

**Core Functionality:**
- Analyze a password string and return a strength rating
- Check for multiple security criteria: length, character diversity, common patterns
- Provide feedback on what makes a password strong or weak

**Requirements:**

1. **Strength Ratings**: Return one of three strength levels:
   - `"weak"`: Fails to meet basic security requirements
   - `"medium"`: Meets some but not all security requirements
   - `"strong"`: Meets all security requirements

2. **Evaluation Criteria**:
   - **Length**: Minimum 8 characters for medium, 12+ for strong
   - **Lowercase letters**: Must contain at least one (a-z)
   - **Uppercase letters**: Must contain at least one (A-Z)
   - **Numbers**: Must contain at least one digit (0-9)
   - **Special characters**: Must contain at least one symbol (!@#$%^&*()_+-=[]{}|;:,.<>?)

3. **Strength Rules**:
   - **Weak**: Less than 8 characters OR missing 3+ character types
   - **Medium**: 8-11 characters with at least 2 character types OR 12+ characters with only 1-2 character types
   - **Strong**: 12+ characters with at least 3 character types

4. **Character Type Detection**: Implement a method that returns which character types are present in the password (lowercase, uppercase, digits, special characters)

**Technical Specifications:**
- Handle empty strings (return "weak")
- Handle unicode characters (treat as special characters if not ASCII letters/digits)
- Case-sensitive analysis
- No external libraries needed (use Python's built-in string methods)

---

## Background Topics

### What is Password Strength?

Password strength measures how resistant a password is to guessing and brute-force attacks. Stronger passwords:
- Take longer to crack through brute force
- Are less likely to be guessed
- Don't appear in common password dictionaries

### Character Types Explained

1. **Lowercase letters (a-z)**: The basic alphabet in lowercase
2. **Uppercase letters (A-Z)**: The basic alphabet in uppercase
3. **Digits (0-9)**: Numeric characters
4. **Special characters**: Symbols like `!@#$%^&*()` that add complexity

### Why Multiple Character Types Matter

Each additional character type increases the "search space" for attackers:
- Only lowercase (26 characters): 26^8 = ~200 billion combinations for 8 chars
- Lowercase + uppercase (52 chars): 52^8 = ~53 trillion combinations
- All types (95 chars): 95^8 = ~6 quadrillion combinations

### Length vs Complexity

Modern security guidance emphasizes **length over complexity**:
- A 16-character password with only lowercase is stronger than an 8-character password with all types
- But practical systems require both for defense-in-depth
