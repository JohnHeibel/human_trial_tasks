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
