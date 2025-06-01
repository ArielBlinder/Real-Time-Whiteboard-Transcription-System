# Real-Time Whiteboard Transcription System - Test Suite

This directory contains a comprehensive test suite for the Real-Time Whiteboard Transcription System. The tests are organized into multiple categories to ensure complete coverage of all application functionality.

## 📁 Test Structure

```
tests/
├── test_boardcast.py        # Main comprehensive test suite (36 tests)
├── test_requirements.txt    # Test dependencies
├── run_tests.py            # Convenience test runner script
├── __init__.py             # Package initialization
└── README.md               # This file
```

## Quick Start

### **Easy Test Runner (Recommended)**

```bash
# Install dependencies first
cd Backend
pip install -r tests/test_requirements.txt

# Run different test categories
python tests/run_tests.py unit --verbose           # Unit tests only
python tests/run_tests.py integration             # Integration tests
python tests/run_tests.py performance             # Performance tests
python tests/run_tests.py all                     # All tests
python tests/run_tests.py quick                   # Fast unit tests
python tests/run_tests.py unit --coverage         # With coverage report
```

### **Manual pytest Commands**

```bash
# From Backend directory
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance"  # Unit tests
python -m pytest tests/test_boardcast.py -v -m "integration"                          # Integration tests
python -m pytest tests/test_boardcast.py -v -m "performance"                          # Performance tests
python -m pytest tests/test_boardcast.py -v                                          # All tests
```

## Test Categories

### **1. Unit Tests (Tests 1-25) - Mocked/Isolated**

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

#### **NVIDIA OCR Unit Tests (Tests 8-12)**

- **Test 8:** `test_nvidia_transcribe_image_success` - Mocked successful NVIDIA API transcription
- **Test 9:** `test_nvidia_transcribe_image_api_failure` - API request failure handling
- **Test 10:** `test_nvidia_transcribe_image_invalid_response` - Invalid API response handling
- **Test 11:** `test_nvidia_transcribe_image_no_api_key` - Missing API key behavior
- **Test 12:** `test_nvidia_transcribe_image_json_error` - Malformed JSON response handling

**Expected Output:**

```
✅ Valid NVIDIA API responses return transcribed text
✅ API failures are handled gracefully with error messages
✅ Invalid responses are caught and handled properly
✅ Missing API keys don't crash the application
✅ JSON decode errors are handled appropriately
```

#### **Frame Processing (Tests 13-14)**

- **Test 13:** `test_process_frame_with_order` - Single frame with order preservation
- **Test 14:** `test_process_video_frames_parallel_success` - Parallel processing integrity

**Expected Output:**

```
✅ Frame order is maintained during processing
✅ Parallel processing returns correct number of results
✅ All frames are processed successfully
```

#### **Gemini Video Processing (Tests 15-17)**

- **Test 15:** `test_process_frames_with_gemini_success` - Mocked Gemini API success
- **Test 16:** `test_process_frames_with_gemini_no_api_key` - API key validation
- **Test 17:** `test_process_frames_with_gemini_empty_frames` - Empty input handling

**Expected Output:**

```
✅ Valid frames return processed content
✅ Missing API key raises ValueError
✅ Empty frames return appropriate message
```

#### **Flask Routes (Tests 18-21)**

- **Test 18:** `test_health_check_endpoint` - Health endpoint functionality
- **Test 19:** `test_system_info_endpoint` - System information endpoint
- **Test 20:** `test_upload_endpoint_no_file` - Missing file handling
- **Test 21:** `test_upload_endpoint_invalid_keys` - API key validation in upload

**Expected Output:**

```
✅ /health returns {"status": "healthy"}
✅ /system-info returns CPU and worker information
✅ Missing file returns 400 error
✅ Invalid API keys return 400 error
```

#### **Dependency Management (Tests 22-23)**

- **Test 22:** `test_check_dependencies_valid` - FFmpeg availability check
- **Test 23:** `test_check_dependencies_missing` - Missing dependency handling

**Expected Output:**

```
✅ Available FFmpeg passes validation
✅ Missing FFmpeg raises DependencyError
```

#### **API Retry Logic (Tests 24-25)**

- **Test 24:** `test_make_api_request_success` - Successful API call
- **Test 25:** `test_make_api_request_rate_limit_retry` - Rate limiting with exponential backoff

**Expected Output:**

```
✅ Successful requests complete on first attempt
✅ Rate limited requests retry with backoff
✅ Exponential delay increases properly
```

### **2. Integration Tests (Tests 26-33) - Real APIs**

These tests require valid API keys and make real API calls. They verify end-to-end functionality.

#### **NVIDIA OCR Integration (Tests 26-28)**

- **Test 26:** `test_nvidia_real_api_integration` - Real NVIDIA API integration with test images
- **Test 27:** `test_nvidia_real_api_complex_image` - Complex image structure handling
- **Test 28:** `test_nvidia_real_api_oversized_image` - Large image handling with real API

**Expected Output:**

```
✅ Real NVIDIA API returns valid string responses
✅ Complex images are processed without errors
✅ Large images are handled gracefully through resizing
⚠️  Requires valid NVIDIA_API_KEY
```

#### **Gemini API Integration (Tests 29-32)**

- **Test 29:** `test_gemini_integration_real_api` - Full Gemini API integration
- **Test 30:** `test_empty_input_real_api` - Empty input with real API
- **Test 31:** `test_invalid_input_real_api` - Invalid input with real API
- **Test 32:** `test_single_frame_real_api` - Single frame with real API

**Expected Output:**

```
✅ Real Gemini API returns cleaned mathematical content
✅ Edge cases handled gracefully
✅ Response contains expected keywords
⚠️  Requires valid OPENROUTER_API_KEY
```

#### **End-to-End Integration (Test 33)**

- **Test 33:** `test_full_pipeline_real_apis` - Complete pipeline: NVIDIA OCR → Gemini processing

**Expected Output:**

```
✅ Full pipeline works with both APIs
✅ OCR results are properly processed by Gemini
✅ End-to-end functionality verified
⚠️  Requires both NVIDIA_API_KEY and OPENROUTER_API_KEY
```

### **3. Performance Tests (Tests 34-36)**

These tests verify system performance and scaling characteristics.

#### **Performance Validation (Tests 34-36)**

- **Test 34:** `test_large_frame_processing_performance` - Large dataset performance
- **Test 35:** `test_worker_scaling_efficiency` - Worker scaling verification
- **Test 36:** `test_nvidia_api_performance` - NVIDIA API response time measurement

**Expected Output:**

```
✅ 50 frames processed in <5 seconds
✅ Multiple workers improve performance
✅ NVIDIA API responds within 10 seconds
✅ No significant overhead from parallelization
```

##  Running the Tests

### **Prerequisites**

```bash
# Install test dependencies
cd Backend
pip install -r tests/test_requirements.txt
```

### **Run All Unit Tests (Recommended)**

```bash
# From Backend directory
python -m pytest tests/test_boardcast.py -v

# Or using our test runner
python tests/run_tests.py unit
```

### **Run Specific Test Categories**

#### **Unit Tests Only (Fast, No API Keys Required)**

```bash
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance"
# Or
python tests/run_tests.py unit
```

#### **Integration Tests (Requires Valid API Keys)**

```bash
python -m pytest tests/test_boardcast.py -v -m "integration"
# Or
python tests/run_tests.py integration
```

#### **Performance Tests**

```bash
python -m pytest tests/test_boardcast.py -v -m "performance"
# Or
python tests/run_tests.py performance
```

#### **All Tests Including Integration**

```bash
python -m pytest tests/test_boardcast.py -v
# Or
python tests/run_tests.py all
```

### **Generate Coverage Report**

```bash
python -m pytest tests/test_boardcast.py --cov=. --cov-report=html --cov-report=term-missing
# Or
python tests/run_tests.py unit --coverage
```

### **Quick Test Run**

```bash
# Fast execution, stop on first failure
python -m pytest tests/test_boardcast.py -x --tb=short
# Or
python tests/run_tests.py quick
```

##  Expected Test Results

### **Successful Run Output:**

```
========================================= test session starts =========================================
platform win32 -- Python 3.12.1, pytest-8.3.5, pluggy-1.6.0
collected 25 items (unit tests only)

TestAPIKeyValidation::test_check_api_keys_valid PASSED                                    [  4%]
TestAPIKeyValidation::test_check_api_keys_invalid PASSED                                  [  8%]
TestWorkerOptimization::test_get_optimal_workers_low_end PASSED                           [ 12%]
TestImageProcessing::test_prepare_image_valid_pil_image PASSED                            [ 16%]
TestNVIDIAOCRUnit::test_nvidia_transcribe_image_success PASSED                            [ 20%]
TestNVIDIAOCRUnit::test_nvidia_transcribe_image_api_failure PASSED                        [ 24%]
...
================================== 25 passed, 11 deselected in 0.68s ==================================
```

### **Coverage Report:**

```
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
app.py                    108     25    77%
process_frames.py          50      8    84%
process_video_text.py      51     12    76%
video_utils.py             54     20    63%
-----------------------------------------------------
TOTAL                     448     65    85%
```

### **Integration Test Output (With Valid API Keys):**

```
TestNVIDIAOCRIntegration::test_nvidia_real_api_integration PASSED                         [ 72%]
TestNVIDIAOCRIntegration::test_nvidia_real_api_complex_image PASSED                       [ 75%]
TestGeminiIntegration::test_gemini_integration_real_api PASSED                            [ 81%]
TestEndToEndIntegration::test_full_pipeline_real_apis PASSED                              [ 91%]
```

##  Configuration

### **API Keys Setup**

For integration tests, ensure API keys are configured in:

- `process_frames.py` - Set `NVIDIA_API_KEY` (get from https://build.nvidia.com/settings/api-keys)
- `process_video_text.py` - Set `OPENROUTER_API_KEY` (get from https://openrouter.ai/settings/keys)

### **Test Markers**

- `@pytest.mark.integration` - Tests requiring real API calls
- `@pytest.mark.performance` - Performance benchmarking tests

### **Skipped Tests**

Integration tests will be automatically skipped if:

- `NVIDIA_API_KEY` is not set or equals "ADD_KEY_HERE" (for NVIDIA OCR tests)
- `OPENROUTER_API_KEY` is not set or equals "ADD_KEY_HERE" (for Gemini tests)

##  Troubleshooting

### **Common Issues:**

1. **Import Errors:**

   ```bash
   # Ensure you're running from the correct directory
   cd Backend/
   python -m pytest tests/test_boardcast.py
   ```

2. **Missing Dependencies:**

   ```bash
   cd Backend
   pip install -r tests/test_requirements.txt
   ```

3. **Integration Tests Failing:**

   - Verify API keys are valid and have sufficient credits
   - Check internet connectivity
   - Some tests may be rate-limited
   - NVIDIA API requires valid subscription/credits

4. **Performance Tests Failing:**
   - Performance tests may vary based on system resources
   - Adjust timing thresholds if needed
   - NVIDIA API performance depends on server load

## 📈 Test Metrics

- **Total Tests:** 36 (25 unit + 8 integration + 3 performance)
- **Code Coverage:** ~85%
- **Execution Time:**
  - Unit tests: ~0.7 seconds
  - Integration tests: ~15-30 seconds (depends on API response times)
  - Performance tests: ~15-20 seconds

##  Best Practices

1. **Run unit tests frequently** during development
2. **Run integration tests** before major releases
3. **Monitor performance tests** for regression detection
4. **Keep API keys secure** and rotate regularly
5. **Test both NVIDIA OCR and Gemini APIs** separately and together
6. **Validate error handling** for both APIs

## 🔄 Continuous Integration

For CI/CD pipelines, use:

```bash
# CI-friendly command (unit tests only)
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance" --tb=short
```

This ensures fast, reliable testing without external dependencies.

##  API Testing Notes

### **NVIDIA OCR API:**

- Uses meta/llama-4-scout-17b-16e-instruct model
- Handles image resizing automatically
- Supports various image formats
- Rate limits may apply based on subscription

### **Gemini API (via OpenRouter):**

- Processes OCR results for cleaning and structuring
- Handles mathematical content well
- Rate limits and costs apply

### **Testing Strategy:**

- **Unit tests** mock all API calls for fast execution
- **Integration tests** use real APIs to verify functionality
- **Performance tests** measure real-world response times
- **End-to-end tests** verify the complete pipeline works
