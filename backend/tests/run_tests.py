#!/usr/bin/env python3
"""
Test Runner for Real-Time Whiteboard Transcription System

This script provides comprehensive testing capabilities including:
- Unit tests execution
- Coverage reporting
- Performance testing
- Integration testing
- API endpoint testing

Usage:
    python run_tests.py [options]
    
Options:
    --unit          Run unit tests only
    --coverage      Run tests with coverage report
    --performance   Run performance tests
    --integration   Run integration tests
    --all           Run all tests (default)
    --verbose       Verbose output
    --parallel      Run tests in parallel
    --html-report   Generate HTML coverage report
"""

import sys
import os
import subprocess
import argparse
import time
from pathlib import Path
import unittest
from unittest.mock import patch

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_command(command, description=""):
    """Run a shell command and return success status"""
    print(f"\n{'='*60}")
    if description:
        print(f"🔧 {description}")
    print(f"Running: {command}")
    print('='*60)
    
    start_time = time.time()
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        elapsed_time = time.time() - start_time
        print(f"\n✅ Command completed successfully in {elapsed_time:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ Command failed after {elapsed_time:.2f}s with exit code {e.returncode}")
        return False

def check_dependencies():
    """Check if required testing dependencies are installed"""
    required_packages = ['unittest', 'coverage', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r test_requirements.txt")
        return False
    
    print("✅ All required testing dependencies are available")
    return True

def run_unit_tests(verbose=False, parallel=False):
    """Run unit tests"""
    print("\n🧪 Running Unit Tests")
    print("-" * 40)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(script_dir, "test_transcription_system.py")
    
    if parallel:
        # Use pytest for parallel execution
        cmd = f'python -m pytest "{test_file}" -v'
        if verbose:
            cmd += " -s"
        cmd += " -n auto"  # Auto-detect number of CPUs
    else:
        # Use unittest
        cmd = f'python "{test_file}"'
        if verbose:
            cmd += " -v"
    
    return run_command(cmd, "Unit Tests")

def run_coverage_tests(html_report=False):
    """Run tests with coverage analysis"""
    print("\n📊 Running Coverage Analysis")
    print("-" * 40)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(script_dir, "test_transcription_system.py")
    parent_dir = os.path.dirname(script_dir)
    
    # Run coverage
    cmd = f'python -m coverage run --source="{parent_dir}" "{test_file}"'
    if not run_command(cmd, "Coverage Test Execution"):
        return False
    
    # Generate coverage report
    cmd = "python -m coverage report -m"
    if not run_command(cmd, "Coverage Report"):
        return False
    
    if html_report:
        cmd = "python -m coverage html"
        if run_command(cmd, "HTML Coverage Report"):
            print("\n📄 HTML coverage report generated in 'htmlcov/' directory")
    
    return True

def run_performance_tests():
    """Run performance tests"""
    print("\n⚡ Running Performance Tests")
    print("-" * 40)
    
    # Simple performance test script
    performance_script = """
import time
import sys
import os
# Add the parent directory (Backend) to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_frames import prepare_image
from PIL import Image

def test_image_processing_performance():
    print("Testing image processing performance...")
    
    # Create test images of different sizes
    test_sizes = [(100, 100), (500, 500), (1000, 1000)]
    
    for width, height in test_sizes:
        img = Image.new('RGB', (width, height), color='red')
        
        start_time = time.time()
        success, result = prepare_image(img)
        elapsed_time = time.time() - start_time
        
        status = "SUCCESS" if success else "FAILED"
        print(f"  {width}x{height} image: {elapsed_time:.4f}s - {status}")

def test_batch_processing_performance():
    print("\\nTesting batch processing performance...")
    
    # Simulate processing multiple frames
    images = [Image.new('RGB', (400, 400), color='blue') for _ in range(10)]
    
    start_time = time.time()
    results = []
    for img in images:
        success, result = prepare_image(img)
        results.append(success)
    elapsed_time = time.time() - start_time
    
    success_count = sum(results)
    print(f"  Processed {len(images)} images in {elapsed_time:.4f}s")
    print(f"  Success rate: {success_count}/{len(images)} ({success_count/len(images)*100:.1f}%)")
    print(f"  Average per image: {elapsed_time/len(images):.4f}s")

if __name__ == "__main__":
    test_image_processing_performance()
    test_batch_processing_performance()
    print("\\nPerformance tests completed")
"""
    
    # Write and run performance test with UTF-8 encoding
    with open("temp_performance_test.py", "w", encoding='utf-8') as f:
        f.write(performance_script)
    
    try:
        success = run_command("python temp_performance_test.py", "Performance Tests")
        return success
    finally:
        # Clean up temporary file
        if os.path.exists("temp_performance_test.py"):
            os.remove("temp_performance_test.py")

def run_integration_tests():
    """Run integration tests"""
    print("\n🔗 Running Integration Tests")
    print("-" * 40)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(script_dir, "test_transcription_system.py")
    
    # Integration test focuses on the TestIntegration class
    cmd = f'python "{test_file}" TestIntegration'
    return run_command(cmd, "Integration Tests")

def run_api_endpoint_tests():
    """Run API endpoint tests"""
    print("\n🌐 Running API Endpoint Tests")
    print("-" * 40)
    
    # Simple API test script
    api_test_script = """
import sys
import os
# Add the parent directory (Backend) to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import patch, Mock
from app import app

def test_health_endpoint():
    print("Testing /health endpoint...")
    with app.test_client() as client:
        response = client.get('/health')
        status = "SUCCESS" if response.status_code == 200 else "FAILED"
        print(f"  Status: {response.status_code} - {status}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"  Response: {data}")

def test_system_info_endpoint():
    print("\\nTesting /system-info endpoint...")
    with app.test_client() as client:
        response = client.get('/system-info')
        status = "SUCCESS" if response.status_code == 200 else "FAILED"
        print(f"  Status: {response.status_code} - {status}")
        if response.status_code == 200:
            data = response.get_json()
            print(f"  CPU Cores: {data.get('cpu_cores', 'N/A')}")
            print(f"  Optimal Workers: {data.get('optimal_workers', 'N/A')}")

if __name__ == "__main__":
    test_health_endpoint()
    test_system_info_endpoint()
    print("\\nAPI endpoint tests completed")
"""
    
    # Write and run API test with UTF-8 encoding
    with open("temp_api_test.py", "w", encoding='utf-8') as f:
        f.write(api_test_script)
    
    try:
        success = run_command("python temp_api_test.py", "API Endpoint Tests")
        return success
    finally:
        # Clean up temporary file
        if os.path.exists("temp_api_test.py"):
            os.remove("temp_api_test.py")

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="Test Runner for Real-Time Whiteboard Transcription System")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--api", action="store_true", help="Run API endpoint tests")
    parser.add_argument("--all", action="store_true", help="Run all tests (default)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run tests in parallel")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML coverage report")
    
    args = parser.parse_args()
    
    # If no specific test type is specified, run all tests
    if not any([args.unit, args.coverage, args.performance, args.integration, args.api]):
        args.all = True
    
    print("🚀 Real-Time Whiteboard Transcription System - Test Runner")
    print("=" * 70)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Track test results
    test_results = []
    start_time = time.time()
    
    try:
        if args.unit or args.all:
            result = run_unit_tests(verbose=args.verbose, parallel=args.parallel)
            test_results.append(("Unit Tests", result))
        
        if args.coverage or args.all:
            result = run_coverage_tests(html_report=args.html_report)
            test_results.append(("Coverage Tests", result))
        
        if args.performance or args.all:
            result = run_performance_tests()
            test_results.append(("Performance Tests", result))
        
        if args.integration or args.all:
            result = run_integration_tests()
            test_results.append(("Integration Tests", result))
        
        if args.api or args.all:
            result = run_api_endpoint_tests()
            test_results.append(("API Endpoint Tests", result))
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Test execution interrupted by user")
        sys.exit(1)
    
    # Print summary
    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print("📋 TEST SUMMARY")
    print("=" * 70)
    
    passed_tests = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20} : {status}")
        if result:
            passed_tests += 1
    
    print(f"\nOverall: {passed_tests}/{len(test_results)} test suites passed")
    print(f"Total execution time: {total_time:.2f}s")
    
    if passed_tests == len(test_results):
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 {len(test_results) - passed_tests} test suite(s) failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 