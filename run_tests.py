import os
import sys
import time
import importlib
import traceback
from pathlib import Path

TEST_DIR = Path("testing")

def discover_tests():
    """Find all test_*.py files in the tests/ directory."""
    return sorted([f.stem for f in TEST_DIR.glob("*.py")])

def run_test_module(module_name):
    """Import and run a test module."""
    print(f"\n=== Running {module_name}.py ===")
    start = time.time()

    try:
        module = importlib.import_module(f"testing.{module_name}")
        if hasattr(module, "run"):
            module.run()
        else:
            # Run all functions
            for attr in dir(module):
                if attr.startswith("test_"):
                    func = getattr(module, attr)
                    print(f" → {attr}()")
                    func()
        duration = (time.time() - start) * 1000
        print(f"✓ {module_name} passed in {duration:.2f}ms")
        return True

    except Exception as e:
        duration = (time.time() - start) * 1000
        print(f"✗ {module_name} FAILED in {duration:.2f}ms")
        print("Error:", e)
        traceback.print_exc()
        return False

def main():
    print("======================================")
    print("     Oil Price API — Test Runner")
    print("======================================")

    tests = discover_tests()
    print(f"Discovered {len(tests)} test modules.")

    passed = 0
    failed = 0

    for test in tests:
        if run_test_module(test):
            passed += 1
        else:
            failed += 1
        time.sleep(0.5)

    print("\n======================================")
    print("               SUMMARY")
    print("======================================")
    print(f" Passed: {passed}")
    print(f" Failed: {failed}")
    print("======================================")

    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
