"""
Real-Time Whiteboard Transcription System - Comprehensive Test Suite

This package contains a complete test suite for the whiteboard transcription system
with 36 tests covering all aspects of the application including NVIDIA OCR integration,
Gemini processing, Flask routes, error handling, and performance validation.

 Test Categories:
- Unit Tests (25): Fast, isolated tests with mocked dependencies
  • API key validation and error handling
  • Worker optimization and system scaling  
  • Image processing and preparation
  • NVIDIA OCR unit tests (mocked API calls)
  • Frame processing and parallel execution
  • Gemini video processing (mocked)
  • Flask routes and endpoint testing
  • Dependency management validation
  • API retry logic and rate limiting

- Integration Tests (8): End-to-end tests with real API calls
  • NVIDIA OCR real API integration
  • Gemini API real integration  
  • End-to-end pipeline testing (NVIDIA → Gemini)
  • Error handling with real APIs

- Performance Tests (3): Benchmarking and scaling validation
  • Large frame processing performance
  • Worker scaling efficiency
  • NVIDIA API response time measurement

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
  - OPENROUTER_API_KEY: For Gemini API integration tests
  
 Performance Targets:
  - Unit tests: <1 second execution
  - Integration tests: <30 seconds (depends on API)
  - Performance tests: <20 seconds
"""

__version__ = "1.0.0"
__author__ = "Ariel Blinder & Saar Attarchi"
__test_count__ = {
    "unit": 25,
    "integration": 8, 
    "performance": 3,
    "total": 36
}
__coverage__ = "~85%"
__last_updated__ = "2024-12-19"
__test_framework__ = "pytest"
__supported_apis__ = ["NVIDIA_NIM", "OpenRouter_Gemini"] 