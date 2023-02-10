## Python code coverage comment

Produces a pull request comment in markdown table format of the code coverage results

## Example output

| Name | Cover | Missing |
| ---  | ----- | ------- |
| **module//file.py** | 98% | 62 |
| **module/file2.py** | 87% | 15,20 |

### Total Coverage: 95%

### Example use

Example workflow could look something like this:

```yaml

jobs:
  testing:
    runs-on: ubuntu-latest
    steps:
      - name: Run coverage
        id: coverage
        run: |
          coverage json --data-file .coverage -o coverage.json
          JSON=$(cat coverage.json)
          echo "coverage=$JSON" >> $GITHUB_OUTPUT
    outputs:
      coverage_report: ${{ steps.coverage.outputs.coverage }}

  results:
    runs-on: ubuntu-latest
    needs: testing
    env:
      COVERAGE_REPORT: ${{ needs.testing.outputs.coverage_report }}
    steps:
      - name: Show coverage results in PR
        uses: Seravo/actions/python-coverage-comment@v0.23
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          coverage-json: ${{ env.COVERAGE_REPORT }}
```