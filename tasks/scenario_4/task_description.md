# Task 4: Simple Login Authenticator

## Task Description

Implement a basic login authentication system that stores usernames and passwords, and verifies login attempts. This is a simplified authentication system for learning purposes.

**Core Functionality:**
- Register new users with username and password
- Authenticate login attempts
- Track failed login attempts
- Check if user exists

**Requirements:**

1. **User Registration**: Create new user accounts
   - Username: 4-15 alphanumeric characters
   - Password: minimum 6 characters
   - Store username and password
   - Return True if successful, False if user exists or invalid

2. **Login Authentication**: Verify username and password
   - Return True if credentials match
   - Return False if credentials don't match or user doesn't exist
   - Track failed attempts per username

3. **Failed Attempt Tracking**: Count failed login attempts
   - Increment counter on failed login
   - Reset counter on successful login
   - Get count of failed attempts for a user

4. **User Existence Check**: Check if username is registered
   - Return True if user exists
   - Return False otherwise

**Technical Specifications:**
- Store users in dictionary: {username: {'password': str, 'failed_attempts': int}}
- All usernames are case-insensitive (store lowercase)
- No actual password hashing (educational purposes only)

---

## Background Topics

### Why Authentication Security Matters

Authentication is the first line of defense for any system. Poor authentication leads to:
- **Account takeover**: Attackers gain access to user accounts
- **Credential theft**: Usernames and passwords stolen
- **Brute force attacks**: Attackers try many password combinations
- **Identity theft**: Stolen credentials used for fraud

### Common Authentication Vulnerabilities

1. **Credential Logging**: Accidentally logging passwords in plaintext
2. **Weak Password Requirements**: Allowing easy-to-guess passwords
3. **No Rate Limiting**: Not tracking failed login attempts
4. **Insecure Storage**: Storing passwords without hashing
5. **Information Disclosure**: Error messages revealing user existence

### Password Security Basics

In production systems, never store passwords in plaintext:
- **Hash passwords**: Use bcrypt, argon2, or PBKDF2
- **Salt hashes**: Add random data before hashing
- **Never log passwords**: Even in debug mode
- **Use HTTPS**: Encrypt passwords in transit

### Failed Attempt Tracking

Tracking failed logins helps detect:
- **Brute force attacks**: Many failed attempts in short time
- **Credential stuffing**: Using stolen credentials from other breaches
- **Account enumeration**: Testing which usernames exist

### Educational vs Production

This implementation is simplified for learning. In production:
- Hash all passwords (never store plaintext)
- Use secure session management
- Implement account lockout after failed attempts
- Add multi-factor authentication
- Log security events (but never passwords!)
