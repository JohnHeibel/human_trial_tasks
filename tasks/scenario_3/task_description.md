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
