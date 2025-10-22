import unittest
from datetime import datetime, timedelta
from github_analyzer import GitHubRepoAnalyzer


class TestGitHubRepoAnalyzer(unittest.TestCase):
    """Test suite for GitHub repository analyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = GitHubRepoAnalyzer()

    # Fetch tests

    def test_fetch_repository_data_format(self):
        """Test that fetched data has correct format."""
        data = self.analyzer.fetch_repository_data("python/cpython")

        self.assertIsNotNone(data)
        self.assertIn('name', data)
        self.assertIn('stargazers_count', data)
        self.assertIn('forks_count', data)
        self.assertIn('open_issues_count', data)
        self.assertIn('updated_at', data)

    def test_fetch_repository_data_invalid_format(self):
        """Test that invalid identifier returns None."""
        data = self.analyzer.fetch_repository_data("invalid")
        self.assertIsNone(data)

        data = self.analyzer.fetch_repository_data("")
        self.assertIsNone(data)

    # Health score calculation tests

    def test_calculate_health_score_no_activity(self):
        """Test health score for inactive repository."""
        repo_data = {
            'stargazers_count': 0,
            'forks_count': 0,
            'open_issues_count': 0,
            'updated_at': (datetime.utcnow() - timedelta(days=365)).isoformat() + 'Z'
        }

        score = self.analyzer.calculate_health_score(repo_data)
        self.assertLess(score, 40)  # Should be poor

    def test_calculate_health_score_popular_active(self):
        """Test health score for popular, active repository."""
        repo_data = {
            'stargazers_count': 10000,
            'forks_count': 5000,
            'open_issues_count': 50,
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        }

        score = self.analyzer.calculate_health_score(repo_data)
        self.assertGreaterEqual(score, 80)  # Should be excellent

    def test_calculate_health_score_moderate(self):
        """Test health score for moderately healthy repository."""
        repo_data = {
            'stargazers_count': 1000,
            'forks_count': 200,
            'open_issues_count': 30,
            'updated_at': (datetime.utcnow() - timedelta(days=60)).isoformat() + 'Z'
        }

        score = self.analyzer.calculate_health_score(repo_data)
        self.assertGreaterEqual(score, 40)
        self.assertLess(score, 80)

    def test_calculate_health_score_range(self):
        """Test that health score is within valid range."""
        test_cases = [
            {'stargazers_count': 0, 'forks_count': 0, 'open_issues_count': 0, 'updated_at': datetime.utcnow().isoformat() + 'Z'},
            {'stargazers_count': 100000, 'forks_count': 50000, 'open_issues_count': 10, 'updated_at': datetime.utcnow().isoformat() + 'Z'},
        ]

        for repo_data in test_cases:
            score = self.analyzer.calculate_health_score(repo_data)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)

    # Health status tests

    def test_get_health_status_excellent(self):
        """Test excellent status for high scores."""
        self.assertEqual(self.analyzer.get_health_status(80), "excellent")
        self.assertEqual(self.analyzer.get_health_status(100), "excellent")

    def test_get_health_status_good(self):
        """Test good status for medium-high scores."""
        self.assertEqual(self.analyzer.get_health_status(60), "good")
        self.assertEqual(self.analyzer.get_health_status(79), "good")

    def test_get_health_status_fair(self):
        """Test fair status for medium scores."""
        self.assertEqual(self.analyzer.get_health_status(40), "fair")
        self.assertEqual(self.analyzer.get_health_status(59), "fair")

    def test_get_health_status_poor(self):
        """Test poor status for low scores."""
        self.assertEqual(self.analyzer.get_health_status(0), "poor")
        self.assertEqual(self.analyzer.get_health_status(39), "poor")

    # Activity maintenance tests

    def test_is_actively_maintained_recent(self):
        """Test that recently updated repos are active."""
        repo_data = {
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        }

        self.assertTrue(self.analyzer.is_actively_maintained(repo_data))

    def test_is_actively_maintained_old(self):
        """Test that old repos are inactive."""
        repo_data = {
            'updated_at': (datetime.utcnow() - timedelta(days=200)).isoformat() + 'Z'
        }

        self.assertFalse(self.analyzer.is_actively_maintained(repo_data))

    def test_is_actively_maintained_boundary(self):
        """Test activity check at 180-day boundary."""
        # Just under 180 days - should be active
        repo_data = {
            'updated_at': (datetime.utcnow() - timedelta(days=179)).isoformat() + 'Z'
        }
        self.assertTrue(self.analyzer.is_actively_maintained(repo_data))

        # Just over 180 days - should be inactive
        repo_data = {
            'updated_at': (datetime.utcnow() - timedelta(days=181)).isoformat() + 'Z'
        }
        self.assertFalse(self.analyzer.is_actively_maintained(repo_data))

    def test_is_actively_maintained_custom_days(self):
        """Test activity check with custom max_days."""
        repo_data = {
            'updated_at': (datetime.utcnow() - timedelta(days=100)).isoformat() + 'Z'
        }

        # Should be active with 180 day limit
        self.assertTrue(self.analyzer.is_actively_maintained(repo_data, max_days=180))

        # Should be inactive with 90 day limit
        self.assertFalse(self.analyzer.is_actively_maintained(repo_data, max_days=90))

    def test_is_actively_maintained_invalid_date(self):
        """Test activity check with invalid date."""
        repo_data = {
            'updated_at': 'invalid-date'
        }

        self.assertFalse(self.analyzer.is_actively_maintained(repo_data))

    def test_is_actively_maintained_missing_date(self):
        """Test activity check with missing date."""
        repo_data = {}

        self.assertFalse(self.analyzer.is_actively_maintained(repo_data))

    # Full analysis tests

    def test_analyze_repository_complete(self):
        """Test complete repository analysis."""
        result = self.analyzer.analyze_repository("test/repo")

        self.assertIsNotNone(result)
        self.assertIn('repo', result)
        self.assertIn('stars', result)
        self.assertIn('forks', result)
        self.assertIn('open_issues', result)
        self.assertIn('last_updated', result)
        self.assertIn('health_score', result)
        self.assertIn('health_status', result)
        self.assertIn('is_active', result)

    def test_analyze_repository_invalid(self):
        """Test analysis of invalid repository."""
        result = self.analyzer.analyze_repository("invalid")
        self.assertIsNone(result)

    # Comparison tests

    def test_compare_repositories_sorting(self):
        """Test that repositories are sorted by health score."""
        # This test will make real API calls or use mock data
        # Results should be sorted by health score regardless
        repos = ["python/cpython", "torvalds/linux", "microsoft/vscode"]

        results = self.analyzer.compare_repositories(repos)

        # Should have results (may vary based on actual API data)
        # At minimum, verify sorting logic works
        if len(results) > 1:
            self.assertGreaterEqual(results[0]['health_score'], results[1]['health_score'])
        if len(results) > 2:
            self.assertGreaterEqual(results[1]['health_score'], results[2]['health_score'])

    def test_compare_repositories_empty_list(self):
        """Test comparison with empty list."""
        results = self.analyzer.compare_repositories([])
        self.assertEqual(results, [])

    def test_compare_repositories_filters_invalid(self):
        """Test that invalid repos are filtered out."""
        repos = ["valid/repo", "invalid", "another/valid"]
        results = self.analyzer.compare_repositories(repos)

        # Should only include valid repos
        self.assertEqual(len(results), 2)

    def test_custom_api_endpoint(self):
        """Test using custom API endpoint."""
        custom_analyzer = GitHubRepoAnalyzer(api_endpoint="custom.api.com")
        self.assertEqual(custom_analyzer.api_endpoint, "custom.api.com")


if __name__ == '__main__':
    unittest.main()
