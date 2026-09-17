import os
import re
from contextlib import suppress
from pathlib import Path

type Rev = str
type DownRev = str
type Revisions = dict[str, Path]
type DownRevisions = dict[str, str | None]


def _unpack_migration_dir(migration_dir: Path) -> list[Path]:
    """Return the migration directory and all of its subdirectories."""
    subdirectories = [
        directory for directory in migration_dir.rglob("*") if directory.is_dir()
    ]
    return [migration_dir, *subdirectories]


def _parse_revision(file: Path) -> tuple[Rev, DownRev | None]:
    """Parse revision from a file. Raises ValueError, if parsing fails."""
    content = file.read_text()
    rev = re.search(
        r"^revision\s*=\s*['\"]([^'\"]+)['\"]",
        content,
        re.MULTILINE,
    )
    # NOTE Alembic merge migrations are currently not supported
    # https://alembic.sqlalchemy.org/en/latest/branches.html#merging-branches
    down_rev = re.search(
        r"^down_revision\s*=\s*['\"]([^'\"]+)['\"]",
        content,
        re.MULTILINE,
    )

    if rev:
        return rev.group(1), down_rev.group(1) if down_rev else None
    raise ValueError(f"File '{file}' is not a revision file")


def _parse_revisions(migration_dirs: list[Path]) -> tuple[Revisions, DownRevisions]:
    """Parse revision IDs and down_revisions from every .py file."""
    revisions = {}
    down_revisions = {}

    for dir in migration_dirs:
        for file in dir.iterdir():
            if file.suffix == ".py":
                with suppress(ValueError):
                    rev, down_rev = _parse_revision(file)
                    revisions[rev] = file
                    down_revisions[rev] = down_rev

    return revisions, down_revisions


def _verify_revisions(revisions: Revisions, down_revisions: DownRevisions) -> int:
    """Verify every down revision actually exists on disk."""
    missing_parents = []
    for rev_id, parent_id in down_revisions.items():
        if parent_id and parent_id not in revisions:
            missing_parents.append((revisions[rev_id], parent_id))

    if missing_parents:
        print("BROKEN LINKS DETECTED:")
        for filepath, missing in missing_parents:
            print(f"  - File {filepath} references missing parent revision: {missing}")
        return 1

    print("All migration files are correctly linked on disk!")
    return 0


def main() -> int:
    """Check that every migration's down_revision exists on disk."""
    migration_dir = Path(os.getenv("MIGRATION_DIR", "migrations"))

    if not migration_dir.is_dir():
        print(f"The given migration dir '{migration_dir}' is not a directory")
        return 1

    migration_dirs = _unpack_migration_dir(migration_dir)
    revisions, down_revisions = _parse_revisions(migration_dirs)
    exit_code = _verify_revisions(revisions, down_revisions)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
