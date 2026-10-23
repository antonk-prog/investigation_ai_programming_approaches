#!/usr/bin/env python3
"""Acceptance checker for the logstat exercise.

Usage:
    python3 shared/acceptance/check.py --bin approaches/01-spec-driven/impl/build/logstat

The checker is intentionally black-box: it only runs the binary and inspects
stdout/stderr/exit code. It does not care how the implementation is structured.
"""

from __future__ import annotations

import argparse
import csv
import io
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "shared" / "fixtures"
HEADER = ["timestamp", "level", "module", "message"]


def csv_rows(text: str) -> list[list[str]]:
    rows = list(csv.reader(io.StringIO(text)))
    return [row for row in rows if row]


def parse_summary(text: str) -> dict:
    result = {
        "total": None,
        "skipped": None,
        "by_level": {},
        "by_module": {},
    }
    section = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("total:"):
            result["total"] = int(line.split(":", 1)[1].strip())
            section = None
        elif line.startswith("by_level:"):
            for token in line.split(":", 1)[1].split():
                if "=" not in token:
                    continue
                key, value = token.split("=", 1)
                result["by_level"][key] = int(value)
            section = None
        elif line.startswith("by_module:"):
            section = "module"
        elif line.startswith("skipped:"):
            result["skipped"] = int(line.split(":", 1)[1].strip())
            section = None
        elif section == "module" and line.startswith("  ") and "=" in line:
            key, value = line.strip().split("=", 1)
            result["by_module"][key] = int(value)
    return result


class Checker:
    def __init__(self, binary: Path):
        self.binary = binary
        self.passed = 0
        self.failed = 0
        self.failures: list[tuple[str, str]] = []

    def run(self, args: list[str]) -> tuple[int, str, str]:
        try:
            proc = subprocess.run(
                [str(self.binary), *args],
                capture_output=True,
                text=True,
                timeout=20,
            )
            return proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            return 124, "", "timeout"
        except OSError as exc:
            return 127, "", str(exc)

    def check(self, name: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed += 1
            print(f"PASS  {name}")
        else:
            self.failed += 1
            self.failures.append((name, detail))
            print(f"FAIL  {name}" + (f"  ({detail})" if detail else ""))

    def detail(self, rc: int, out: str, err: str) -> str:
        return (
            f"rc={rc}; "
            f"stdout={out[:160]!r}; "
            f"stderr={err[:160]!r}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a logstat implementation")
    parser.add_argument("--bin", required=True, help="path to the logstat binary")
    args = parser.parse_args()

    binary = Path(args.bin)
    if not binary.exists():
        print(f"error: binary not found: {binary}", file=sys.stderr)
        return 2
    if not binary.is_file():
        print(f"error: not a file: {binary}", file=sys.stderr)
        return 2

    resolved = binary.resolve()
    if not resolved.stat().st_mode & 0o111 and not shutil.which(str(resolved)):
        print(f"error: binary is not executable: {resolved}", file=sys.stderr)
        return 2

    c = Checker(resolved)
    sample = str(FIX / "sample.csv")
    malformed = str(FIX / "malformed.csv")
    empty = str(FIX / "empty.csv")
    quoting = str(FIX / "quoting.csv")
    missing = str(FIX / "does-not-exist.csv")

    # 1. help
    rc, out, err = c.run(["--help"])
    c.check(
        "help exits 0",
        rc == 0,
        c.detail(rc, out, err),
    )
    c.check(
        "help mentions logstat and usage",
        "logstat" in (out + err).lower() and "usage" in (out + err).lower(),
        c.detail(rc, out, err),
    )

    # 2. no arguments
    rc, out, err = c.run([])
    c.check("no arguments exits 2", rc == 2, c.detail(rc, out, err))

    # 3. default output
    rc, out, err = c.run([sample])
    rows = csv_rows(out)
    c.check("sample exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "sample header",
        bool(rows) and rows[0] == HEADER,
        f"header={rows[0] if rows else None}",
    )
    c.check(
        "sample has 12 data rows",
        len(rows) == 13,
        f"rows={len(rows)}",
    )

    # 4. time range
    rc, out, err = c.run(
        [sample, "--from", "2026-10-01T09:00:00", "--to", "2026-10-01T10:30:00"]
    )
    rows = csv_rows(out)
    timestamps = [r[0] for r in rows[1:]] if rows else []
    expected_ts = {
        "2026-10-01T09:00:00",
        "2026-10-01T09:30:00",
        "2026-10-01T10:00:00",
        "2026-10-01T10:15:00",
        "2026-10-01T10:30:00",
    }
    c.check("time range exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "time range selects 5 rows",
        len(rows) == 6 and set(timestamps) == expected_ts,
        f"rows={len(rows)} ts={timestamps}",
    )

    # 5. min-level
    rc, out, err = c.run([sample, "--min-level", "WARN"])
    rows = csv_rows(out)
    levels = {r[1] for r in rows[1:]} if rows else set()
    c.check("min-level WARN exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "min-level WARN selects 5 rows of WARN/ERROR",
        len(rows) == 6 and levels <= {"WARN", "ERROR"} and len(levels) > 0,
        f"rows={len(rows)} levels={levels}",
    )

    # 6. module
    rc, out, err = c.run([sample, "--module", "can"])
    rows = csv_rows(out)
    modules = {r[2] for r in rows[1:]} if rows else set()
    c.check("module can exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "module can selects 4 rows",
        len(rows) == 5 and modules == {"can"},
        f"rows={len(rows)} modules={modules}",
    )

    # 7. combined filters
    rc, out, err = c.run(
        [
            sample,
            "--from",
            "2026-10-01T09:00:00",
            "--min-level",
            "ERROR",
            "--module",
            "can",
        ]
    )
    rows = csv_rows(out)
    c.check("combined filters exit 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "combined filters select 1 row at 09:30",
        len(rows) == 2 and rows[1][0] == "2026-10-01T09:30:00",
        f"rows={len(rows)} data={rows[1:] if rows else None}",
    )

    # 8. no matches
    rc, out, err = c.run([sample, "--module", "missing"])
    rows = csv_rows(out)
    c.check("no matches exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "no matches prints only header",
        rows == [HEADER],
        f"rows={rows}",
    )

    # 9. empty input
    rc, out, err = c.run([empty])
    rows = csv_rows(out)
    c.check("empty input exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "empty input prints only header",
        rows == [HEADER],
        f"rows={rows}",
    )

    # 10. malformed, non-strict
    rc, out, err = c.run([malformed])
    rows = csv_rows(out)
    c.check("malformed non-strict exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "malformed non-strict keeps 3 valid rows",
        len(rows) == 4 and {r[1] for r in rows[1:]} == {"INFO", "WARN", "ERROR"},
        f"rows={len(rows)} data={rows[1:]}",
    )
    c.check(
        "malformed non-strict warns on stderr",
        err.strip() != "",
        f"stderr={err!r}",
    )

    # 11. malformed, strict
    rc, out, err = c.run([malformed, "--strict"])
    c.check("malformed strict exits 2", rc == 2, c.detail(rc, out, err))

    # 12. summary of sample
    rc, out, err = c.run([sample, "--summary"])
    summary = parse_summary(out)
    c.check("summary exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "summary total is 12",
        summary["total"] == 12,
        f"summary={summary}",
    )
    c.check(
        "summary by_level is exact",
        summary["by_level"]
        == {"TRACE": 1, "DEBUG": 2, "INFO": 4, "WARN": 2, "ERROR": 3},
        f"by_level={summary['by_level']}",
    )
    c.check(
        "summary by_module is exact and sorted",
        summary["by_module"] == {"io": 5, "can": 4, "power": 3},
        f"by_module={summary['by_module']}",
    )
    c.check(
        "summary skipped is 0",
        summary["skipped"] == 0,
        f"skipped={summary['skipped']}",
    )

    # 13. summary of malformed
    rc, out, err = c.run([malformed, "--summary"])
    summary = parse_summary(out)
    c.check("malformed summary exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "malformed summary total 3 / skipped 3",
        summary["total"] == 3 and summary["skipped"] == 3,
        f"summary={summary}",
    )

    # 14. quoting
    rc, out, err = c.run([quoting])
    rows = csv_rows(out)
    c.check("quoting exits 0", rc == 0, c.detail(rc, out, err))
    c.check(
        "quoting round-trips commas and quotes",
        len(rows) == 3
        and rows[1][3] == 'Comm "lost", retrying'
        and rows[2][3] == "plain",
        f"rows={rows}",
    )

    # 15. missing file
    rc, out, err = c.run([missing])
    c.check(
        "missing file exits 2 with stderr",
        rc == 2 and err.strip() != "",
        c.detail(rc, out, err),
    )

    # 16. invalid date
    rc, out, err = c.run([sample, "--from", "2026-13-01T00:00:00"])
    c.check("invalid date exits 2", rc == 2, c.detail(rc, out, err))

    # 17. invalid level
    rc, out, err = c.run([sample, "--min-level", "LOUD"])
    c.check("invalid level exits 2", rc == 2, c.detail(rc, out, err))

    # 18. unknown option
    rc, out, err = c.run([sample, "--nope"])
    c.check("unknown option exits 2", rc == 2, c.detail(rc, out, err))

    total = c.passed + c.failed
    percent = (c.passed / total * 100.0) if total else 0.0
    print()
    print(f"{c.passed}/{total} passed ({percent:.1f}%), {c.failed} failed")
    if c.failures:
        print("\nFailures:")
        for name, detail in c.failures:
            print(f"  - {name}: {detail}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
