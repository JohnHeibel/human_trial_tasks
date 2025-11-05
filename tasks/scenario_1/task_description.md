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
