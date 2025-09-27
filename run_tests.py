#!/usr/bin/env python3
"""
Test runner for gifverse project
"""

import sys
import subprocess
import os

def run_tests():
    """Run the test suite"""
    print("Running gifverse test suite...")
    print("=" * 50)

    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    try:
        # Run pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--color=yes"
        ], check=True)

        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        return 0

    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Tests failed!")
        return e.returncode
    except FileNotFoundError:
        print("❌ pytest not found. Please install it with: pip install pytest")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
