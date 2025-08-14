#!/usr/bin/env python3
"""
Quality check script for the research agent project.
Runs formatting, linting, type checking, and tests.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔍 {description}...")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} passed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Run all quality checks."""
    print("🚀 Running quality checks for research agent...")

    # Change to project directory
    project_root = Path(__file__).parent
    original_cwd = Path.cwd()

    try:
        # Change to project directory
        import os

        os.chdir(project_root)

        checks = [
            (["uv", "run", "ruff", "format", "--check", "."], "Code formatting check"),
            (["uv", "run", "ruff", "check", "."], "Linting check"),
            (["uv", "run", "mypy", ".", "--ignore-missing-imports"], "Type checking"),
            (
                [
                    "uv",
                    "run",
                    "pytest",
                    "tests/",
                    "-v",
                    "--cov=.",
                    "--cov-report=term-missing",
                ],
                "Test suite",
            ),
        ]

        passed = 0
        total = len(checks)

        for cmd, description in checks:
            if run_command(cmd, description):
                passed += 1

        print(f"\n📊 Results: {passed}/{total} checks passed")

        if passed == total:
            print("🎉 All quality checks passed!")
            return 0
        else:
            print("💥 Some quality checks failed!")
            return 1

    finally:
        # Restore original directory
        os.chdir(original_cwd)


if __name__ == "__main__":
    sys.exit(main())
