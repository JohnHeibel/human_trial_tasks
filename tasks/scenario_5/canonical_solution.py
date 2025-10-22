import urllib.request
import urllib.error
import json
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional


class GitHubRepoAnalyzer:
    """Analyzes GitHub repositories for health and activity metrics."""
    
    def __init__(self, api_endpoint: str = "api.github.com"):
        """
        Initialize the GitHub repository analyzer.

        Args:
            api_endpoint: GitHub API endpoint (default: "api.github.com")
        """
        self.api_endpoint = api_endpoint
    
    def fetch_repository_data(self, repo_identifier: str) -> Optional[Dict[str, Any]]:
        """
        Fetch repository data from GitHub API.

        Args:
            repo_identifier: Repository in format "owner/repo"

        Returns:
            Dictionary with repository data or None if fetch fails
        """
        # Validate format
        if '/' not in repo_identifier:
            return None

        try:
            # Construct URL
            url = f"https://{self.api_endpoint}/repos/{repo_identifier}"

            # Create request with User-Agent header
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'GitHub-Repo-Analyzer/1.0'}
            )

            # Make API call
            response = urllib.request.urlopen(req, timeout=10)
            data = json.loads(response.read().decode('utf-8'))

            return data

        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, TimeoutError):
            return None
    
    def calculate_health_score(self, repo_data: Dict[str, Any]) -> int:
        """
        Calculate repository health score (0-100).
        
        Args:
            repo_data: Repository data dictionary
            
        Returns:
            Health score between 0 and 100
        """
        score = 0
        
        # Star score (0-40 points): logarithmic scale
        stars = repo_data.get('stargazers_count', 0)
        if stars > 0:
            star_score = min(40, math.log10(stars + 1) * 10)
            score += star_score
        
        # Activity score (0-30 points): based on last update
        updated_at = repo_data.get('updated_at', '')
        if updated_at:
            try:
                last_update = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc)
                days_since_update = (now - last_update).days
                
                if days_since_update < 30:
                    score += 30
                elif days_since_update < 90:
                    score += 20
                elif days_since_update < 180:
                    score += 10
            except (ValueError, AttributeError):
                pass
        
        # Issue ratio score (0-15 points): fewer issues is better
        open_issues = repo_data.get('open_issues_count', 0)
        issue_ratio = open_issues / (stars + 1)
        if issue_ratio < 0.01:
            score += 15
        elif issue_ratio < 0.05:
            score += 10
        elif issue_ratio < 0.1:
            score += 5
        
        # Fork ratio score (0-15 points): more forks is better
        forks = repo_data.get('forks_count', 0)
        fork_ratio = forks / (stars + 1)
        if fork_ratio > 0.5:
            score += 15
        elif fork_ratio > 0.2:
            score += 10
        elif fork_ratio > 0.1:
            score += 5
        
        return min(100, int(score))
    
    def get_health_status(self, score: int) -> str:
        """
        Convert health score to status string.
        
        Args:
            score: Health score (0-100)
            
        Returns:
            Status: "excellent", "good", "fair", or "poor"
        """
        if score >= 80:
            return "excellent"
        elif score >= 60:
            return "good"
        elif score >= 40:
            return "fair"
        else:
            return "poor"
    
    def analyze_repository(self, repo_identifier: str) -> Optional[Dict[str, Any]]:
        """
        Perform complete analysis of a repository.
        
        Args:
            repo_identifier: Repository in format "owner/repo"
            
        Returns:
            Dictionary with analysis results or None if fetch fails
        """
        repo_data = self.fetch_repository_data(repo_identifier)
        
        if not repo_data:
            return None
        
        health_score = self.calculate_health_score(repo_data)
        health_status = self.get_health_status(health_score)
        is_active = self.is_actively_maintained(repo_data)
        
        return {
            'repo': repo_identifier,
            'stars': repo_data.get('stargazers_count', 0),
            'forks': repo_data.get('forks_count', 0),
            'open_issues': repo_data.get('open_issues_count', 0),
            'last_updated': repo_data.get('updated_at', ''),
            'health_score': health_score,
            'health_status': health_status,
            'is_active': is_active
        }
    
    def is_actively_maintained(self, repo_data: Dict[str, Any], max_days: int = 180) -> bool:
        """
        Check if repository is actively maintained.
        
        Args:
            repo_data: Repository data dictionary
            max_days: Maximum days since last update (default: 180)
            
        Returns:
            True if active, False otherwise
        """
        updated_at = repo_data.get('updated_at', '')
        
        if not updated_at:
            return False
        
        try:
            last_update = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            days_since_update = (now - last_update).days
            
            return days_since_update <= max_days
        except (ValueError, AttributeError):
            return False
    
    def compare_repositories(self, repo_identifiers: List[str]) -> List[Dict[str, Any]]:
        """
        Compare multiple repositories and sort by health score.
        
        Args:
            repo_identifiers: List of repository identifiers
            
        Returns:
            List of analysis results sorted by health score (descending)
        """
        results = []
        
        for repo_id in repo_identifiers:
            analysis = self.analyze_repository(repo_id)
            if analysis:
                results.append(analysis)
        
        # Sort by health score (descending)
        results.sort(key=lambda x: x['health_score'], reverse=True)

        return results