#!/usr/bin/env python3
"""
Test Runner Script for Real-Time Whiteboard Transcription System

This script provides convenient commands to run different categories of tests.
"""

import subprocess
import sys
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n🚀 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run tests for the whiteboard transcription system")
    parser.add_argument(
        "category",
        choices=["unit", "integration", "performance", "all", "quick"],
        help="Test category to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Run with verbose output"
    )

    args = parser.parse_args()

    # Change to the Backend directory if we're in tests/
    if Path.cwd().name == "tests":
        import os
        os.chdir("..")

    base_cmd = "python -m pytest tests/test_boardcast.py"
    
    if args.verbose:
        base_cmd += " -v"
    
    if args.coverage:
        base_cmd += " --cov=. --cov-report=html --cov-report=term-missing"

    commands = {
        "unit": (
            f'{base_cmd} -m "not integration and not performance"',
            "Running Unit Tests (Fast, No API Keys Required)"
        ),
        "integration": (
            f'{base_cmd} -m "integration"',
            "Running Integration Tests (Requires Valid API Keys)"
        ),
        "performance": (
            f'{base_cmd} -m "performance"',
            "Running Performance Tests"
        ),
        "all": (
            base_cmd,
            "Running All Tests (Unit + Integration + Performance)"
        ),
        "quick": (
            f'{base_cmd} -x --tb=short -m "not integration and not performance"',
            "Running Quick Unit Tests (Stop on First Failure)"
        )
    }

    cmd, description = commands[args.category]
    success = run_command(cmd, description)

    if success:
        print(f"\n✅ {description} completed successfully!")
    else:
        print(f"\n❌ {description} failed!")
        sys.exit(1)

    # Print helpful information
    print(f"\n💡 Test Categories Available:")
    print(f"   • unit: Fast unit tests with mocked dependencies")
    print(f"   • integration: End-to-end tests with real API calls")
    print(f"   • performance: Performance benchmarking tests")
    print(f"   • all: Run everything")
    print(f"   • quick: Fast unit tests, stop on first failure")
    
    if args.coverage:
        print(f"\n📊 Coverage report generated in htmlcov/index.html")

if __name__ == "__main__":
    main() 