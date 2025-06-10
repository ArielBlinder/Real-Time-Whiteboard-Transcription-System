#!/usr/bin/env python3

# Test Runner for BoardCast

import subprocess
import sys
from pathlib import Path

def main():
    # Change to the backend directory if we're in tests/
    if Path.cwd().name == "tests":
        import os
        os.chdir("..")

    print(" Running All Tests in test_boardcast.py")
    print("=" * 60)
    print(" Total Tests: 25 (18 unit + 4 integration + 1 performance + 2 edge cases)")
    print()

    # Simple command - just run all tests in test_boardcast.py
    cmd = "python -m pytest tests/test_boardcast.py --tb=short"
    
    try:
        # Run the tests and let pytest handle all output
        result = subprocess.run(cmd, shell=True)
        
        if result.returncode == 0:
            print("\n   All tests completed successfully!")
            print("\n   Test Coverage:")
            print("   • API Integration (NVIDIA OCR + Gemini)")
            print("   • Image & Video Processing") 
            print("   • Error Handling & Edge Cases")
            print("   • Performance & Parallel Processing")
            print("   • Flask Routes & Dependencies")
            
        else:
            print("\n   Some tests failed!")
            print("\n   Common Issues:")
            print("   • Set NVIDIA_API_KEY for integration tests")
            print("   • Set GEMINI_API_KEY for Google AI Studio tests") 
            print("   • Install FFmpeg for dependency tests")
            print("   • Check internet connection for API tests")
            
        return result.returncode
        
    except Exception as e:
        print(f" Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 