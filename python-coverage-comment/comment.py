import json
import os
import sys
from typing import List

import requests
from coverage_typing import Coverage


def coverage_to_markdown(coverage: Coverage) -> List[str]:
    """Convert coverage data to a human readable markdown table"""
    table = [
        "## Code Coverage Report",
        "",
        "| Name | Cover | Missing |",
        "| ---  | ----- | ------- |"
    ]

    covered_total = 0
    missing_total = 0

    for filename, cov in coverage['files'].items():
        # Append totals
        covered_total += len(cov["executed_lines"])
        missing_total += len(cov['missing_lines'])

        # Skip 100% covered files
        if not cov['missing_lines']:
            continue

        # Add new line after 50 characters
        missing_lines = []
        row = 0
        for line in map(str, cov['missing_lines']):
            row += len(line)
            if row > 50:
                line = "<br>" + line
                row = 0
            missing_lines.append(line)

        cover = cov['summary']['percent_covered_display']
        missing = ",".join(missing_lines)
        table.append(f"| **{filename}** | {cover}% | {missing} |")

    total_lines = covered_total + missing_total
    table.append("")
    table.append(f"### Total Coverage: {covered_total/total_lines*100:.1f}%")

    return table


def main() -> int:
    """Load coverage data and send it as a comment to the pull request"""
    # Read set configuration
    BASE_URL = os.getenv('GITHUB_URL', "https://api.github.com")
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    OWNER = os.getenv('OWNER')
    REPOSITORY = os.getenv('REPOSITORY')
    ISSUE_NUMBER = os.getenv('ISSUE_NUMBER')
    COVERAGE_JSON = os.getenv('COVERAGE_JSON')

    # Load coverage
    try:
        coverage: Coverage = json.loads(COVERAGE_JSON)
    except json.JSONDecodeError as e:
        print(f"Bad JSON input: {str(e)}")
        return 1

    table = coverage_to_markdown(coverage)
    # Print markdown table for step summary
    print("\n".join(table))
    body = {'body': "\n".join(table)}

    # Send the comment
    url = f"{BASE_URL}/repos/{OWNER}/{REPOSITORY}/issues/{ISSUE_NUMBER}/comments"
    headers = {
        'Authorization': f"Bearer {GITHUB_TOKEN}",
        'Accept': "application/vnd.github+json",
        'X-GitHub-Api-Version': "2022-11-28"
    }
    try:
        res = requests.post(url, json=body, headers=headers)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to create a comment: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
