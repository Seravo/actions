from typing import Dict, List, TypedDict


class CoverageMeta(TypedDict):
    """Coverage metadata"""
    version: str
    timestamp: str
    branch_coverage: bool
    show_contexts: bool


class FileCoverageSummary(TypedDict):
    """A single file's coverage summary"""
    covered_lines: int
    num_statements: int
    percent_covered: float
    percent_covered_display: str
    missing_lines: int
    excluded_lines: int


class FileCoverage(TypedDict):
    """A single file's coverage results"""
    executed_lines: List[int]
    missing_lines: List[int]
    excluded_lines: List[int]
    summary: FileCoverageSummary


class Coverage(TypedDict):
    """Coverage results dict"""
    meta: CoverageMeta
    files: Dict[str, FileCoverage]
