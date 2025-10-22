from typing import Dict, Any, Optional


class RateLimiter:
    """Tracks and enforces rate limits for users."""

    def __init__(self, max_requests: int = 100):
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum number of requests allowed per user (default: 100)
        """
        # TODO: Store the max_requests limit
        # TODO: Initialize a dictionary to track request counts per user
        pass

    def check_rate_limit(self, user_id: str, request_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if a request should be allowed and increment counter if so.

        Args:
            user_id: Unique identifier for the user
            request_data: Optional dictionary containing request metadata
                         (e.g., {'endpoint': '/api/data', 'method': 'GET', 'ip': '192.168.1.1'})

        Returns:
            True if request is allowed (under limit), False if blocked (at or over limit)
        """
        # TODO: Handle None request_data by setting to empty dict
        # TODO: Get current count for this user (default to 0 if not present)
        # TODO: Check if current count is at or above max_requests
        #       - If so, return False (blocked)
        # TODO: If under limit, increment the counter and return True (allowed)
        pass

    def get_request_count(self, user_id: str) -> int:
        """
        Get the current request count for a user.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Number of requests made by this user
        """
        # TODO: Return the count for this user (default to 0 if not present)
        pass

    def reset_user(self, user_id: str) -> None:
        """
        Reset the request counter for a specific user.

        Args:
            user_id: Unique identifier for the user
        """
        # TODO: Remove this user from the request_counts dictionary
        # Hint: Check if user exists before removing to avoid KeyError
        pass

    def reset_all(self) -> None:
        """Reset all request counters."""
        # TODO: Clear all entries from the request_counts dictionary
        pass
