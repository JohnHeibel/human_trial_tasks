import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_key_manager import APIKeyManager


class TestAPIKeyManager(unittest.TestCase):
    """Test suite for API key manager."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = APIKeyManager()

    def test_generate_key_format(self):
        """Test that generated keys have correct format."""
        metadata = {'user_id': 'user1', 'email': 'user1@example.com'}
        key = self.manager.generate_key(metadata)

        # Should start with default prefix
        self.assertTrue(key.startswith('sk_'))

        # Should be prefix + 32 hex characters = 35 total
        self.assertEqual(len(key), 35)

        # Characters after prefix should be valid hex
        hex_part = key[3:]  # Remove 'sk_' prefix
        self.assertTrue(all(c in '0123456789abcdef' for c in hex_part))

    def test_validate_generated_key(self):
        """Test that generated keys validate successfully."""
        metadata = {'user_id': 'user3', 'email': 'user3@example.com'}
        key = self.manager.generate_key(metadata)

        # Key should be valid
        self.assertTrue(self.manager.validate_key(key))

    def test_validate_invalid_key(self):
        """Test that invalid keys are rejected."""
        # Generate a valid key, then modify it to make it invalid
        metadata = {'user_id': 'test_invalid'}
        valid_key = self.manager.generate_key(metadata)

        # Modify the key by changing the last character to ensure it's invalid
        invalid_key = valid_key[:-1] + ('0' if valid_key[-1] != '0' else '1')

        self.assertFalse(self.manager.validate_key(invalid_key))

    def test_validate_empty_key(self):
        """Test validation of empty string."""
        self.assertFalse(self.manager.validate_key(""))

    def test_get_metadata(self):
        """Test retrieving metadata for a key."""
        metadata = {
            'user_id': 'user4',
            'email': 'user4@example.com',
            'permissions': ['read', 'write']
        }
        key = self.manager.generate_key(metadata)

        retrieved_metadata = self.manager.get_metadata(key)

        self.assertIsNotNone(retrieved_metadata)
        self.assertEqual(retrieved_metadata['user_id'], 'user4')
        self.assertEqual(retrieved_metadata['email'], 'user4@example.com')
        self.assertEqual(retrieved_metadata['permissions'], ['read', 'write'])

    def test_get_metadata_invalid_key(self):
        """Test getting metadata for non-existent key."""
        metadata = self.manager.get_metadata("sk_nonexistent")
        self.assertIsNone(metadata)

    def test_revoke_key(self):
        """Test revoking an API key."""
        metadata = {'user_id': 'user5'}
        key = self.manager.generate_key(metadata)

        # Key should be valid initially
        self.assertTrue(self.manager.validate_key(key))

        # Revoke the key
        result = self.manager.revoke_key(key)
        self.assertTrue(result)

        # Key should no longer be valid
        self.assertFalse(self.manager.validate_key(key))

    def test_revoke_nonexistent_key(self):
        """Test revoking a key that doesn't exist."""
        result = self.manager.revoke_key("sk_nonexistent")
        self.assertFalse(result)

    def test_list_user_keys_single_user(self):
        """Test listing keys for a user with multiple keys."""
        user_id = 'user6'

        # Generate 1 key for the user
        key1 = self.manager.generate_key({'user_id': user_id, 'name': 'key1'})

        user_keys = self.manager.list_user_keys(user_id)

        # Should have at least 1 key
        self.assertGreaterEqual(len(user_keys), 1)
        self.assertIn(key1, user_keys)

    def test_list_user_keys_multiple_users(self):
        """Test that user key listing is isolated per user."""
        # Generate key for user7
        key1 = self.manager.generate_key({'user_id': 'user7'})

        user7_keys = self.manager.list_user_keys('user7')
        user8_keys = self.manager.list_user_keys('user8')

        # User 7 should have 1 key
        self.assertEqual(len(user7_keys), 1)
        self.assertIn(key1, user7_keys)

        # User 8 should have 0 keys
        self.assertEqual(len(user8_keys), 0)

    def test_list_user_keys_no_keys(self):
        """Test listing keys for user with no keys."""
        user_keys = self.manager.list_user_keys('nonexistent_user')
        self.assertEqual(user_keys, [])

    def test_get_all_keys(self):
        """Test getting all active keys."""
        # Generate a key
        key1 = self.manager.generate_key({'user_id': 'user9'})

        all_keys = self.manager.get_all_keys()

        # Should have at least 1 key
        self.assertGreaterEqual(len(all_keys), 1)
        self.assertIn(key1, all_keys)

    def test_custom_prefix(self):
        """Test API key manager with custom prefix."""
        custom_manager = APIKeyManager(prefix="pk_")

        metadata = {'user_id': 'user12'}
        key = custom_manager.generate_key(metadata)

        # Should start with custom prefix
        self.assertTrue(key.startswith('pk_'))
        self.assertEqual(len(key), 35)  # pk_ + 32 hex chars

    def test_metadata_isolation(self):
        """Test that modifying original metadata doesn't affect stored metadata."""
        metadata = {'user_id': 'user13', 'count': 0}
        key = self.manager.generate_key(metadata)

        # Modify original metadata
        metadata['count'] = 100
        metadata['new_field'] = 'added'

        # Stored metadata should be unchanged
        stored_metadata = self.manager.get_metadata(key)
        self.assertEqual(stored_metadata['count'], 0)
        self.assertNotIn('new_field', stored_metadata)

    def test_revoke_and_list_keys(self):
        """Test that revoked keys don't appear in listings."""
        user_id = 'user15'
        key1 = self.manager.generate_key({'user_id': user_id})

        # Verify key is in list
        user_keys = self.manager.list_user_keys(user_id)
        self.assertIn(key1, user_keys)

        # Revoke the key
        self.manager.revoke_key(key1)

        # Verify key is no longer in list
        user_keys = self.manager.list_user_keys(user_id)
        self.assertNotIn(key1, user_keys)

    def test_complex_metadata(self):
        """Test storing and retrieving complex metadata."""
        metadata = {
            'user_id': 'user16',
            'email': 'user16@example.com',
            'permissions': ['read', 'write', 'delete'],
            'created_at': '2024-01-01T00:00:00Z',
            'rate_limit': 1000,
            'is_active': True,
            'tags': {'environment': 'production', 'team': 'engineering'}
        }

        key = self.manager.generate_key(metadata)
        retrieved = self.manager.get_metadata(key)

        self.assertEqual(retrieved['user_id'], 'user16')
        self.assertEqual(retrieved['permissions'], ['read', 'write', 'delete'])
        self.assertEqual(retrieved['rate_limit'], 1000)
        self.assertTrue(retrieved['is_active'])
        self.assertEqual(retrieved['tags']['environment'], 'production')

    def test_empty_metadata(self):
        """Test generating key with empty metadata."""
        key = self.manager.generate_key({})

        self.assertTrue(self.manager.validate_key(key))
        metadata = self.manager.get_metadata(key)
        self.assertEqual(metadata, {})

    def test_multiple_revocations(self):
        """Test revoking the same key multiple times."""
        metadata = {'user_id': 'user17'}
        key = self.manager.generate_key(metadata)

        # First revocation should succeed
        self.assertTrue(self.manager.revoke_key(key))

        # Second revocation should fail (key already gone)
        self.assertFalse(self.manager.revoke_key(key))


if __name__ == '__main__':
    unittest.main()
