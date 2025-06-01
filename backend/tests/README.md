# Real-Time Whiteboard Transcription System - Test Suite

This directory contains a comprehensive test suite for the Real-Time Whiteboard Transcription System. The tests are organized into multiple categories to ensure complete coverage of all application functionality.

##  Test Structure

```
tests/
├── test_boardcast.py        # Main comprehensive test suite (27 tests)
├── test_requirements.txt    # Test dependencies
├── run_tests.py            # Convenience test runner script
├── pytest.ini             # Pytest configuration
├── __init__.py             # Package initialization
└── README.md               # This file
```

##  Quick Start

### **Easy Test Runner (Recommended)**

```bash
# Install dependencies first
cd backend
cd tests
pip install -r test_requirements.txt

# Run different test categories
python run_tests.py unit --verbose           # Unit tests only
python run_tests.py integration             # Integration tests
python run_tests.py performance             # Performance tests
python run_tests.py all                     # All tests
python run_tests.py quick                   # Fast unit tests
python run_tests.py unit --coverage         # With coverage report
```

### **Manual pytest Commands**

```bash
# From Backend directory
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance"  # Unit tests
python -m pytest tests/test_boardcast.py -v -m "integration"                          # Integration tests
python -m pytest tests/test_boardcast.py -v -m "performance"                          # Performance tests
python -m pytest tests/test_boardcast.py -v                                          # All tests
```

##  Test Categories

### **1. Unit Tests (Tests 1-21) - Mocked/Isolated**

These tests run quickly and don't require real API keys. They use mocks to simulate external dependencies.

#### **API Key Validation (Tests 1-2)**

- **Test 1:** `test_check_api_keys_valid` - Validates proper API key detection
- **Test 2:** `test_check_api_keys_invalid` - Ensures invalid keys are properly rejected

**Expected Output:**

```
✅ Valid keys return (True, "")
✅ Invalid keys return (False, "error message with URLs")
```

#### **Worker Optimization (Tests 3-4)**

- **Test 3:** `test_get_optimal_workers_low_end` - Low-end system (2 cores → 4 workers)
- **Test 4:** `test_get_optimal_workers_high_end` - High-end system (16 cores → 20 workers)

**Expected Output:**

```
✅ Worker count scales with CPU cores
✅ Minimum 2 workers guaranteed
✅ Maximum caps prevent resource exhaustion
```

#### **Image Processing (Tests 5-7)**

- **Test 5:** `test_prepare_image_valid_pil_image` - PIL image to base64 conversion
- **Test 6:** `test_prepare_image_invalid_input` - Handles non-existent files gracefully
- **Test 7:** `test_prepare_image_large_image` - Resizes large images properly

**Expected Output:**

```
✅ Valid images return (True, base64_string)
✅ Invalid inputs return (False, error_message)
✅ Large images are resized maintaining aspect ratio
```

#### **Frame Processing (Tests 8-9)**

- **Test 8:** `test_process_frame_with_order` - Single frame with order preservation
- **Test 9:** `test_process_video_frames_parallel_success` - Parallel processing integrity

**Expected Output:**

```
✅ Frame order is maintained during processing
✅ Parallel processing returns correct number of results
✅ All frames are processed successfully
```

#### **Video Processing (Tests 10-12)**

- **Test 10:** `test_process_frames_with_gemini_success` - Mocked Gemini API success
- **Test 11:** `test_process_frames_with_gemini_no_api_key` - API key validation
- **Test 12:** `test_process_frames_with_gemini_empty_frames` - Empty input handling

**Expected Output:**

```
✅ Valid frames return processed content
✅ Missing API key raises ValueError
✅ Empty frames return appropriate message
```

#### **Flask Routes (Tests 13-16)**

- **Test 13:** `test_health_check_endpoint` - Health endpoint functionality
- **Test 14:** `test_system_info_endpoint` - System information endpoint
- **Test 15:** `test_upload_endpoint_no_file` - Missing file handling
- **Test 16:** `test_upload_endpoint_invalid_keys` - API key validation in upload

**Expected Output:**

```
✅ /health returns {"status": "healthy"}
✅ /system-info returns CPU and worker information
✅ Missing file returns 400 error
✅ Invalid API keys return 400 error
```

#### **Dependency Management (Tests 17-18)**

- **Test 17:** `test_check_dependencies_valid` - FFmpeg availability check
- **Test 18:** `test_check_dependencies_missing` - Missing dependency handling

**Expected Output:**

```
✅ Available FFmpeg passes validation
✅ Missing FFmpeg raises DependencyError
```

#### **API Retry Logic (Tests 19-20)**

- **Test 19:** `test_make_api_request_success` - Successful API call
- **Test 20:** `test_make_api_request_rate_limit_retry` - Rate limiting with exponential backoff

**Expected Output:**

```
✅ Successful requests complete on first attempt
✅ Rate limited requests retry with backoff
✅ Exponential delay increases properly
```

#### **Image Transcription (Test 21)**

- **Test 21:** `test_transcribe_image_success` - Mocked NVIDIA API transcription

**Expected Output:**

```
✅ Valid images return transcribed text
✅ API integration works correctly
```

### **2. Integration Tests (Tests 22-25) - Real APIs**

These tests require valid API keys and make real API calls. They verify end-to-end functionality.

#### **Real API Integration (Tests 22-25)**

- **Test 22:** `test_gemini_integration_real_api` - Full Gemini API integration
- **Test 23:** `test_empty_input_real_api` - Empty input with real API
- **Test 24:** `test_invalid_input_real_api` - Invalid input with real API
- **Test 25:** `test_single_frame_real_api` - Single frame with real API

**Expected Output:**

```
✅ Real API returns cleaned mathematical content
✅ Edge cases handled gracefully
✅ Response contains expected keywords
⚠️  Requires valid OPENROUTER_API_KEY
```

### **3. Performance Tests (Tests 26-27)**

These tests verify system performance and scaling characteristics.

#### **Performance Validation (Tests 26-27)**

- **Test 26:** `test_large_frame_processing_performance` - Large dataset performance
- **Test 27:** `test_worker_scaling_efficiency` - Worker scaling verification

**Expected Output:**

```
✅ 50 frames processed in <5 seconds
✅ Multiple workers improve performance
✅ No significant overhead from parallelization
```

## 🚀 Running the Tests

### **Prerequisites**

```bash
# Install test dependencies
cd tests/
pip install -r test_requirements.txt
```

### **Run All Unit Tests (Recommended)**

```bash
# From Backend directory
python -m pytest tests/test_boardcast.py -v

# Or from tests directory
python -m pytest test_boardcast.py -v
```

### **Run Specific Test Categories**

#### **Unit Tests Only (Fast, No API Keys Required)**

```bash
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance"
```

#### **Integration Tests (Requires Valid API Keys)**

```bash
python -m pytest tests/test_boardcast.py -v -m "integration"
```

#### **Performance Tests**

```bash
python -m pytest tests/test_boardcast.py -v -m "performance"
```

#### **All Tests Including Integration**

```bash
python -m pytest tests/test_boardcast.py -v -m "integration or not integration"
```

### **Generate Coverage Report**

```bash
python -m pytest tests/test_boardcast.py --cov=.. --cov-report=html --cov-report=term-missing
```

### **Quick Test Run**

```bash
# Fast execution, stop on first failure
python -m pytest tests/test_boardcast.py -x --tb=short
```

## 📊 Expected Test Results

### **Successful Run Output:**

```
========================================= test session starts =========================================
platform win32 -- Python 3.12.1, pytest-8.3.5, pluggy-1.6.0
collected 21 items (unit tests only)

TestAPIKeyValidation::test_check_api_keys_valid PASSED                                    [  4%]
TestAPIKeyValidation::test_check_api_keys_invalid PASSED                                  [  9%]
TestWorkerOptimization::test_get_optimal_workers_low_end PASSED                           [ 14%]
...
========================================= 21 passed in 0.45s ==========================================
```

### **Coverage Report:**

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app.py                    108     37    66%
process_frames.py          50     11    78%
process_video_text.py      51     14    73%
video_utils.py             54     28    48%
-----------------------------------------------------
TOTAL                     448     91    80%
```

### **Integration Test Output (With Valid API Keys):**

```
TestRealAPIIntegration::test_gemini_integration_real_api PASSED                           [ 81%]
TestRealAPIIntegration::test_empty_input_real_api PASSED                                  [ 86%]
TestRealAPIIntegration::test_single_frame_real_api PASSED                                 [ 95%]
```

## 🔧 Configuration

### **API Keys Setup**

For integration tests, ensure API keys are configured in:

- `process_video_text.py` - Set `OPENROUTER_API_KEY`
- `process_frames.py` - Set `NVIDIA_API_KEY`

### **Test Markers**

- `@pytest.mark.integration` - Tests requiring real API calls
- `@pytest.mark.performance` - Performance benchmarking tests

### **Skipped Tests**

Integration tests will be automatically skipped if:

- `OPENROUTER_API_KEY` is not set
- `OPENROUTER_API_KEY` equals "ADD_KEY_HERE"

## 🐛 Troubleshooting

### **Common Issues:**

1. **Import Errors:**

   ```bash
   # Ensure you're running from the correct directory
   cd Backend/
   python -m pytest tests/test_boardcast.py
   ```

2. **Missing Dependencies:**

   ```bash
   pip install -r tests/test_requirements.txt
   ```

3. **Integration Tests Failing:**

   - Verify API keys are valid and have sufficient credits
   - Check internet connectivity
   - Some tests may be rate-limited

4. **Performance Tests Failing:**
   - Performance tests may vary based on system resources
   - Adjust timing thresholds if needed

## 📈 Test Metrics

- **Total Tests:** 27 (21 unit + 4 integration + 2 performance)
- **Code Coverage:** ~80%
- **Execution Time:**
  - Unit tests: ~0.5 seconds
  - Integration tests: ~5-10 seconds
  - Performance tests: ~10-15 seconds

## 💡 Best Practices

1. **Run unit tests frequently** during development
2. **Run integration tests** before major releases
3. **Monitor performance tests** for regression detection
4. **Update tests** when adding new features
5. **Keep API keys secure** and rotate regularly

## 🔄 Continuous Integration

For CI/CD pipelines, use:

```bash
# CI-friendly command (unit tests only)
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance" --tb=short
```

This ensures fast, reliable testing without external dependencies.
