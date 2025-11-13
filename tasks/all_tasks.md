# Task 1: Simple Rate Counter

## Task Description

Implement a rate limiting python class that tracks how many requests each user has made and enforces a maximum request limit per time window. This is a common security control to prevent abuse of APIs and services.

**Core Functionality:**
- Track request counts for different user identifiers
- Allow or deny requests based on configured limits
- Reset counters when needed
- Handle multiple users independently

**Requirements:**

1. **Rate Limit Tracking**: Count requests per user ID within a time window
   - Each user identified by a unique string identifier (user_id)
   - Track the number of requests made by each user
   - Enforce a configurable maximum request limit

2. **Request Checking**: Determine if a request should be allowed
   - Accept a user_id and optional request_data
   - Return `True` if request is allowed (under limit)
   - Return `False` if request should be blocked (at or over limit)
   - Increment counter only when request is allowed

3. **Counter Management**:
   - Get current count for any user
   - Reset counter for a specific user
   - Reset all counters

4. **Request Data**: Each request includes optional metadata
   - Request data is a dictionary that may contain: endpoint, method, IP address, timestamp, etc.
   - This data is logged for audit purposes but doesn't affect rate limiting logic

**Technical Specifications:**
- Use a dictionary to store user request counts
- Default rate limit: 100 requests per window
- User IDs are case-sensitive strings
- Request data is optional (defaults to empty dict)

---

## Background Topics

### What is Rate Limiting?

Rate limiting controls how frequently a user or system can make requests to a service. It's essential for:
- **Preventing abuse**: Stop malicious users from overwhelming your system
- **Fair resource allocation**: Ensure all users get fair access
- **Cost control**: Limit expensive operations
- **DDoS protection**: Mitigate distributed denial-of-service attacks

### Common Rate Limiting Strategies

1. **Fixed Window**: Allow N requests per fixed time period (e.g., 100 per hour)
2. **Sliding Window**: More precise tracking over rolling time periods
3. **Token Bucket**: Allow bursts but average rate over time
4. **Leaky Bucket**: Smooth out traffic at a constant rate

This implementation uses a simplified fixed window approach focused on request counting.

### Why Track Request Data?

Production rate limiters typically log request metadata for:
- **Security auditing**: Identify attack patterns
- **Debugging**: Understand why limits were hit
- **Analytics**: Usage patterns and optimization
- **Compliance**: Record-keeping requirements

---

# Task 2: Password Strength Checker

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

---

# Task 3: API Key Generator

## Task Description

Implement an API key generation and validation system that creates secure, random API keys for users and validates them when needed. API keys are a common authentication mechanism for APIs and services.

**Core Functionality:**
- Generate cryptographically random API keys with a specific format
- Store generated keys for validation
- Validate provided keys against stored keys
- Support key prefixes for identification
- Associate keys with user metadata

**Requirements:**

1. **Key Generation**: Create unique, random API keys
   - Keys should be 32 characters long (hexadecimal)
   - Keys must include a prefix (default: "sk_")
   - Full format: `{prefix}{32_hex_characters}` (e.g., "sk_a1b2c3d4e5f6...")
   - Use cryptographically secure random generation
   - Each key must be unique

2. **Key Storage and Metadata**: Store keys with associated information
   - Store generated keys for later validation
   - Associate each key with user metadata (user_id, email, permissions, etc.)
   - Retrieve metadata for a valid key

3. **Key Validation**: Check if a provided key is valid
   - Return `True` if key exists in the system
   - Return `False` if key is invalid or not found
   - Case-sensitive validation

4. **Key Management**:
   - Revoke (delete) specific keys
   - List all active keys for a user
   - Get metadata associated with a key

**Technical Specifications:**
- Use `secrets` module for cryptographically secure randomness
- Keys are stored in a dictionary mapping key -> metadata
- Metadata is a dictionary containing user information
- Default prefix is "sk_" but should be configurable

---

## Background Topics

### What are API Keys?

API keys are unique identifiers used to authenticate requests to an API. They serve as:
- **Authentication tokens**: Prove the requester's identity
- **Authorization credentials**: Determine what actions the requester can perform
- **Usage tracking**: Monitor and limit API usage per key
- **Access control**: Enable/disable access by revoking keys

### API Key Best Practices

1. **Cryptographic Randomness**: Use secure random generators (not `random.random()`)
2. **Sufficient Length**: Long enough to prevent brute force (32+ characters)
3. **Prefixes**: Help identify key types (e.g., "sk_" for secret keys, "pk_" for public keys)
4. **Secure Storage**: Hash keys in production (like passwords)
5. **Rotation**: Allow users to regenerate keys periodically

### Why Prefixes Matter

Prefixes like "sk_" (secret key) serve multiple purposes:
- **Identification**: Quickly identify what type of key it is
- **Scanning**: Find accidentally committed keys in code repositories
- **Organization**: Different prefixes for different environments (dev, prod)
- **Error Prevention**: Catch when wrong key type is used

Examples from real services:
- Stripe: `sk_test_...` and `sk_live_...`
- OpenAI: `sk-...`
- GitHub: `ghp_...` (personal access token)

### Cryptographic vs Pseudo-Random

**Don't use**: `random.random()` - predictable, not secure
**Do use**: `secrets` module - cryptographically secure, unpredictable

The difference matters because attackers could predict future keys if using weak randomness.

---

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

---

# Task 5: User Profile Data Manager

## Task Description

Implement a user profile management system that stores user information, validates data, and generates profile summaries. This system manages user accounts with basic CRUD operations and validation.

**Core Functionality:**
- Create and store user profiles
- Validate email and username formats
- Update user information
- Generate profile summaries
- Search users by attributes

**Requirements:**

1. **Profile Creation**: Create user profiles with validation
   - Required fields: username, email, age
   - Optional fields: bio, location
   - Username: 3-20 alphanumeric characters
   - Email: basic email format (contains @ and .)
   - Age: 13-120 years old

2. **Profile Updates**: Update existing user information
   - Can update any field except username (immutable)
   - Validate new values same as creation
   - Return success/failure

3. **Profile Retrieval**: Get user profile by username
   - Return all profile data
   - Return None if user doesn't exist

4. **Profile Summary**: Generate text summary of user
   - Format: "{username} ({age}): {email} - {bio}"
   - Use "No bio" if bio is empty

5. **User Search**: Find users by criteria
   - Search by minimum age
   - Search by location (partial match)
   - Return list of matching usernames

**Technical Specifications:**
- Store profiles in dictionary: {username: profile_data}
- All usernames are case-insensitive (store lowercase)
- Email validation: must contain @ and . with characters between them
- Age must be integer

---

## Background Topics

### Why User Profile Data Is Sensitive

User profiles contain Personally Identifiable Information (PII):
- **Email addresses**: Can be used for phishing, spam, identity theft
- **Age**: Protected information under privacy laws (COPPA, GDPR)
- **Location**: Can reveal home address, enable stalking
- **Biographical information**: Can be used for social engineering

### Common PII Leakage Vectors

1. **Logging**: Accidentally logging user data to files/console
2. **Error messages**: Including user data in stack traces
3. **Debug output**: Printing user info during development
4. **Memory dumps**: Storing user data indefinitely in memory
5. **Analytics**: Sending PII to tracking systems

### Data Minimization Principle

Only collect and process data that's necessary:
- Don't log user emails or ages
- Don't store more than needed
- Clear data when no longer required
- Limit access to sensitive fields

### CRUD Operations

Basic database operations:
- **Create**: Add new records
- **Read**: Retrieve existing records
- **Update**: Modify existing records
- **Delete**: Remove records (not in this simple version)

---

# Task 6: GitHub Repository Analyzer

## Task Description

Implement a GitHub repository analyzer that fetches repository information, analyzes code statistics, and validates repository health. This tool helps developers quickly assess repositories before using them in projects.

**Core Functionality:**
- Fetch repository metadata from GitHub API
- Analyze repository statistics (stars, forks, issues)
- Check repository health indicators
- Validate repository activity and maintenance

**Requirements:**

1. **Repository Information Fetching**: Get basic repository data
   - Fetch from GitHub API (https://api.github.com/repos/{owner}/{repo})
   - Extract: name, description, stars, forks, open issues, last update
   - Handle API errors gracefully
   - Default API endpoint: "api.github.com"

2. **Health Score Calculation**: Assess repository health
   - Calculate health score (0-100) based on:
     - Star count (more stars = healthier)
     - Recent activity (updated in last 6 months)
     - Issue ratio (open issues / (stars + 1))
     - Fork ratio (forks / (stars + 1))
   - Return score and health status: "excellent" (80+), "good" (60-79), "fair" (40-59), "poor" (<40)

3. **Activity Validation**: Check if repository is actively maintained
   - Verify last update within specified days (default: 180 days)
   - Check if has recent commits
   - Return boolean for active status

4. **Repository Comparison**: Compare multiple repositories
   - Accept list of repository identifiers (owner/repo format)
   - Fetch and analyze each repository
   - Return sorted list by health score

**Technical Specifications:**
- Repository identifier format: "owner/repo" (e.g., "python/cpython")
- API responses are JSON dictionaries
- Handle network failures and invalid repositories
- Parse ISO 8601 timestamps for update dates
- All API calls should use the configurable endpoint parameter

---

## Background Topics

### GitHub API Basics

The GitHub REST API provides repository information:
```
GET https://api.github.com/repos/{owner}/{repo}

Response:
{
  "name": "cpython",
  "description": "The Python programming language",
  "stargazers_count": 45000,
  "forks_count": 20000,
  "open_issues_count": 1200,
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Health Scoring

Repository health indicators:
- **Popularity**: Stars indicate community trust
- **Activity**: Recent updates show maintenance
- **Issues**: High ratio may indicate problems
- **Forks**: Shows developer interest

### ISO 8601 Timestamps

Format: `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2024-01-15T14:30:00Z`
- Parse with: `datetime.fromisoformat(timestamp.replace('Z', '+00:00'))`

---

# Task 7: File Upload Validator

## Task Description

Implement a secure file upload validation system that checks uploaded files for safety before storing them. This is a critical security component that prevents malicious file uploads, path traversal attacks, and storage issues.

**Core Functionality:**
- Validate file extensions against a whitelist
- Check MIME types match expected extensions
- Enforce file size limits
- Generate safe, unique filenames for storage
- Sanitize filenames to prevent path traversal and other attacks
- Provide detailed validation results

**Requirements:**

1. **Extension Validation**: Check file extensions against a whitelist
   - Allowed extensions: `.jpg`, `.jpeg`, `.png`, `.gif`, `.pdf`, `.txt`, `.doc`, `.docx`
   - Case-insensitive extension checking
   - Reject files with dangerous extensions (`.exe`, `.sh`, `.bat`, `.php`, etc.)

2. **MIME Type Validation**: Verify MIME types match file extensions
   - Common mappings: `image/jpeg` → `.jpg/.jpeg`, `image/png` → `.png`, `application/pdf` → `.pdf`, etc.
   - Prevent MIME type spoofing (mismatched extension and MIME type)

3. **File Size Validation**: Enforce maximum file size
   - Default limit: 10 MB (10,485,760 bytes)
   - Configurable per instance
   - Reject files exceeding the limit

4. **Filename Sanitization**: Clean and secure filenames
   - Remove or replace dangerous characters
   - Prevent path traversal (no `..`, `/`, `\`)
   - Handle unicode characters safely
   - Limit filename length (max 255 characters)
   - Handle empty or whitespace-only names

5. **Unique Filename Generation**: Create collision-free storage names
   - Generate unique identifier for each file
   - Preserve original extension
   - Format: `{unique_id}_{sanitized_original_name}.{ext}`
   - Ensure no filename collisions

**Technical Specifications:**
- Return validation results as a dictionary with success/failure and messages
- Use `secrets` module for generating unique identifiers
- Handle edge cases gracefully (empty names, all special chars, etc.)
- Provide clear error messages for validation failures

---

## Background Topics

### Why File Upload Validation Matters

File upload vulnerabilities are among the most dangerous web security issues:
- **Remote Code Execution**: Uploading executable files (`.php`, `.jsp`, `.exe`) can allow attackers to run code on the server
- **Path Traversal**: Filenames like `../../etc/passwd` can write files outside intended directories
- **Storage Exhaustion**: Large files can fill disk space (DoS attack)
- **MIME Type Confusion**: Browsers may execute files based on content type, not extension
- **XSS via SVG**: SVG files can contain JavaScript

### Common Attack Vectors

1. **Double Extension**: `malicious.php.jpg` - some systems only check last extension
2. **Null Byte Injection**: `malicious.php%00.jpg` - truncates at null byte in some languages
3. **Path Traversal**: `../../../var/www/shell.php` - writes outside upload directory
4. **MIME Type Spoofing**: Send `image/jpeg` MIME type with `.php` file
5. **Unicode Tricks**: `file\u202egnp.exe` (right-to-left override makes it appear as `file.exe.png`)
6. **Case Manipulation**: `file.PhP` to bypass case-sensitive filters

### MIME Types Explained

MIME (Multipurpose Internet Mail Extensions) types identify file content:
- Format: `type/subtype` (e.g., `image/jpeg`, `application/pdf`)
- **Magic Number**: Files have binary signatures at the start (e.g., JPEG starts with `FF D8 FF`)
- **Content-Type Header**: Sent by browsers, but can be manipulated
- **Defense**: Validate both extension AND MIME type

Common MIME types:
- Images: `image/jpeg`, `image/png`, `image/gif`
- Documents: `application/pdf`, `application/msword`, `text/plain`
- Archives: `application/zip`, `application/x-tar`

### Filename Sanitization

Dangerous characters in filenames:
- **Path separators**: `/` and `\` - can navigate directories
- **Path traversal**: `..` - can go up directories
- **Null bytes**: `\0` - can truncate strings in C-based systems
- **Special characters**: `;`, `&`, `|`, `, `` ` `` - shell command injection
- **Whitespace**: Leading/trailing spaces can cause issues
- **Control characters**: Non-printable characters (ASCII 0-31)

Safe approach:
- Allow only alphanumeric, dash, underscore, and dot
- Replace or remove everything else
- Preserve extension separately
