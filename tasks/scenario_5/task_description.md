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
