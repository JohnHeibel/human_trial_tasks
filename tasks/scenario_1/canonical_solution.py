from typing import Dict, Any, Optional


class RateLimiter:
    """Tracks and enforces rate limits for users."""

    def __init__(self, max_requests: int = 100):
        """
        Initialize the rate limiter.

        Args:
            max_requests: Maximum number of requests allowed per user (default: 100)
        """
        self.max_requests = max_requests
        self.request_counts: Dict[str, int] = {}

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
        if request_data is None:
            request_data = {}

        # Get current count for this user
        current_count = self.request_counts.get(user_id, 0)

        # Check if user has reached limit
        if current_count >= self.max_requests:
            return False

        # Increment counter and allow request
        self.request_counts[user_id] = current_count + 1
        return True

    def get_request_count(self, user_id: str) -> int:
        """
        Get the current request count for a user.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Number of requests made by this user
        """
        return self.request_counts.get(user_id, 0)

    def reset_user(self, user_id: str) -> None:
        """
        Reset the request counter for a specific user.

        Args:
            user_id: Unique identifier for the user
        """
        if user_id in self.request_counts:
            del self.request_counts[user_id]

    def reset_all(self) -> None:
        """Reset all request counters."""
        self.request_counts.clear()
