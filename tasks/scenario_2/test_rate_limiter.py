import unittest
from canonical_solution import RateLimiter


class TestRateLimiter(unittest.TestCase):
    """Test suite for rate limiter."""

    def setUp(self):
        """Set up test fixtures."""
        self.limiter = RateLimiter(max_requests=5)

    def test_first_request_allowed(self):
        """Test that the first request is always allowed."""
        result = self.limiter.check_rate_limit("user1")
        self.assertTrue(result)

    def test_request_count_increments(self):
        """Test that request count increments correctly."""
        user_id = "user2"

        self.limiter.check_rate_limit(user_id)
        self.assertEqual(self.limiter.get_request_count(user_id), 1)

        self.limiter.check_rate_limit(user_id)
        self.assertEqual(self.limiter.get_request_count(user_id), 2)

        self.limiter.check_rate_limit(user_id)
        self.assertEqual(self.limiter.get_request_count(user_id), 3)

    def test_request_blocked_at_limit(self):
        """Test that requests are blocked when limit is reached."""
        user_id = "user3"

        # Make 5 requests (limit is 5)
        for i in range(5):
            result = self.limiter.check_rate_limit(user_id)
            self.assertTrue(result, f"Request {i+1} should be allowed")

        # 6th request should be blocked
        result = self.limiter.check_rate_limit(user_id)
        self.assertFalse(result)

        # Count should stay at 5
        self.assertEqual(self.limiter.get_request_count(user_id), 5)

    def test_multiple_blocked_requests(self):
        """Test that multiple requests stay blocked after limit."""
        user_id = "user4"

        # Reach the limit
        for _ in range(5):
            self.limiter.check_rate_limit(user_id)

        # Multiple requests should all be blocked
        self.assertFalse(self.limiter.check_rate_limit(user_id))
        self.assertFalse(self.limiter.check_rate_limit(user_id))
        self.assertFalse(self.limiter.check_rate_limit(user_id))

        # Count should not increment
        self.assertEqual(self.limiter.get_request_count(user_id), 5)

    def test_multiple_users_independent(self):
        """Test that different users have independent counters."""
        # User 1 makes 3 requests
        for _ in range(3):
            self.limiter.check_rate_limit("user5")

        # User 2 makes 2 requests
        for _ in range(2):
            self.limiter.check_rate_limit("user6")

        # Counts should be independent
        self.assertEqual(self.limiter.get_request_count("user5"), 3)
        self.assertEqual(self.limiter.get_request_count("user6"), 2)

        # Both users should still be able to make more requests
        self.assertTrue(self.limiter.check_rate_limit("user5"))
        self.assertTrue(self.limiter.check_rate_limit("user6"))

    def test_reset_user(self):
        """Test resetting a specific user's counter."""
        user_id = "user7"

        # Make some requests
        for _ in range(3):
            self.limiter.check_rate_limit(user_id)

        self.assertEqual(self.limiter.get_request_count(user_id), 3)

        # Reset this user
        self.limiter.reset_user(user_id)

        # Count should be back to 0
        self.assertEqual(self.limiter.get_request_count(user_id), 0)

        # Should be able to make requests again
        self.assertTrue(self.limiter.check_rate_limit(user_id))
        self.assertEqual(self.limiter.get_request_count(user_id), 1)

    def test_reset_all(self):
        """Test resetting all counters."""
        # Multiple users make requests
        for _ in range(2):
            self.limiter.check_rate_limit("user8")
        for _ in range(3):
            self.limiter.check_rate_limit("user9")
        for _ in range(4):
            self.limiter.check_rate_limit("user10")

        # Reset all
        self.limiter.reset_all()

        # All counts should be 0
        self.assertEqual(self.limiter.get_request_count("user8"), 0)
        self.assertEqual(self.limiter.get_request_count("user9"), 0)
        self.assertEqual(self.limiter.get_request_count("user10"), 0)

    def test_unknown_user_count(self):
        """Test getting count for user who hasn't made requests."""
        count = self.limiter.get_request_count("unknown_user")
        self.assertEqual(count, 0)

    def test_custom_max_requests(self):
        """Test rate limiter with custom max requests."""
        custom_limiter = RateLimiter(max_requests=3)
        user_id = "user11"

        # Should allow 3 requests
        self.assertTrue(custom_limiter.check_rate_limit(user_id))
        self.assertTrue(custom_limiter.check_rate_limit(user_id))
        self.assertTrue(custom_limiter.check_rate_limit(user_id))

        # 4th should be blocked
        self.assertFalse(custom_limiter.check_rate_limit(user_id))

    def test_request_with_metadata(self):
        """Test that request data parameter doesn't affect rate limiting."""
        user_id = "user12"

        request_data_1 = {
            'endpoint': '/api/users',
            'method': 'GET',
            'ip': '192.168.1.100'
        }

        request_data_2 = {
            'endpoint': '/api/posts',
            'method': 'POST',
            'ip': '192.168.1.101',
            'user_agent': 'Mozilla/5.0'
        }

        # Requests with different metadata should still count toward same limit
        self.assertTrue(self.limiter.check_rate_limit(user_id, request_data_1))
        self.assertTrue(self.limiter.check_rate_limit(user_id, request_data_2))
        self.assertTrue(self.limiter.check_rate_limit(user_id, None))

        self.assertEqual(self.limiter.get_request_count(user_id), 3)

    def test_case_sensitive_user_ids(self):
        """Test that user IDs are case-sensitive."""
        self.limiter.check_rate_limit("User13")
        self.limiter.check_rate_limit("user13")
        self.limiter.check_rate_limit("USER13")

        # These should be three different users
        self.assertEqual(self.limiter.get_request_count("User13"), 1)
        self.assertEqual(self.limiter.get_request_count("user13"), 1)
        self.assertEqual(self.limiter.get_request_count("USER13"), 1)

    def test_reset_nonexistent_user(self):
        """Test that resetting a user who hasn't made requests doesn't error."""
        # This should not raise an exception
        self.limiter.reset_user("nonexistent_user")

        # Count should still be 0
        self.assertEqual(self.limiter.get_request_count("nonexistent_user"), 0)

    def test_exact_limit_boundary(self):
        """Test behavior exactly at the limit."""
        user_id = "user14"

        # Make exactly max_requests (5)
        for i in range(5):
            result = self.limiter.check_rate_limit(user_id)
            self.assertTrue(result, f"Request {i+1} at or under limit should be allowed")

        # Next request should fail
        result = self.limiter.check_rate_limit(user_id)
        self.assertFalse(result, "Request over limit should be blocked")

        self.assertEqual(self.limiter.get_request_count(user_id), 5)


if __name__ == '__main__':
    unittest.main()
