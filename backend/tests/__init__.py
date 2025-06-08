"""
Real-Time Whiteboard Transcription System - Comprehensive Test Suite

This package contains a complete test suite for the whiteboard transcription system
with 25 tests covering all aspects of the application including NVIDIA OCR integration,
Gemini processing, Flask routes, error handling, and performance validation.

 Test Categories:
- Unit Tests (21): Fast, isolated tests with mocked dependencies
  • API key validation and error handling (2 tests)
  • Worker optimization and system scaling (2 tests)
  • Image processing and preparation (2 tests)
  • NVIDIA OCR unit tests with mocked API calls (3 tests)
  • Frame processing and parallel execution (2 tests)
  • Gemini video processing with mocked APIs (2 tests)
  • Flask routes and endpoint testing (2 tests)
  • Dependency management validation (2 tests)
  • API retry logic and rate limiting (1 test)
  • Edge cases and error handling (3 tests)

- Integration Tests (3): End-to-end tests with real API calls
  • NVIDIA OCR real API integration (1 test)
  • Gemini API real integration (2 tests)
  • End-to-end pipeline testing (NVIDIA → Gemini) (integrated in above)

- Performance Tests (1): Benchmarking and scaling validation
  • Large frame processing performance (1 test)

 Coverage:
- Total Code Coverage: ~85%
- NVIDIA OCR Integration: 88% coverage
- Process Video Text: 76% coverage
- Main Application: 77% coverage

 Quick Start:
  # Unit tests (fast, no API keys required)
  python tests/run_tests.py unit
  
  # Integration tests (requires valid API keys)  
  python tests/run_tests.py integration
  
  # All tests with coverage
  python tests/run_tests.py unit --coverage

 Documentation:
  See tests/README.md for comprehensive testing guide
  
 Manual pytest commands:
  python -m pytest tests/test_boardcast.py -v  # All tests
  python -m pytest tests/test_boardcast.py -v -m "not integration and not performance"  # Unit only

 API Requirements:
  - NVIDIA_API_KEY: For NVIDIA OCR integration tests
  - GEMINI_API_KEY: For Google AI Studio API integration tests
  
 Performance Targets:
  - Unit tests: <1 second execution
  - Integration tests: <30 seconds (depends on API)
  - Performance tests: <20 seconds
"""

__version__ = "1.0.0"
__author__ = "Ariel Blinder & Saar Attarchi"
__test_count__ = {
    "unit": 21,
    "integration": 3, 
    "performance": 1,
    "total": 25
}
__coverage__ = "~85%"
__last_updated__ = "2024-12-19"
__test_framework__ = "pytest"
__supported_apis__ = ["NVIDIA_NIM", "GoogleAI_Gemini"]