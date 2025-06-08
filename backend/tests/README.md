# Real-Time Whiteboard Transcription System (BoardCast) - Test Suite

This directory contains a comprehensive test suite for BoardCast, The tests are organized into multiple categories to ensure complete coverage of all application functionality.

## Test Structure

```
tests/
├── test_boardcast.py        # Main comprehensive test suite (25 tests)
├── test_requirements.txt    # Test dependencies
├── run_tests.py            # Ultra-simple test runner script
├── __init__.py             # Package initialization
└── README.md               # This file
```

## Quick Start

### **Simple Test Runner (Only Way)**

```bash
# Install dependencies first
cd backend
pip install -r tests/test_requirements.txt

# Run ALL 25 tests
python tests/run_tests.py
```

**That's it!** No arguments, no options, no complexity. The script automatically:

- Runs all 25 tests in `test_boardcast.py`
- Provides clear output and error messages
- Shows test coverage summary
- Gives troubleshooting tips if tests fail

### **Advanced: Direct pytest (For Developers)**

If you need granular control, you can still use pytest directly:

```bash
# From backend directory
python -m pytest tests/test_boardcast.py -v                                          # All tests (verbose)
python -m pytest tests/test_boardcast.py -v -m "not integration and not performance"  # Unit tests only
python -m pytest tests/test_boardcast.py -v -m "integration"                          # Integration tests only
python -m pytest tests/test_boardcast.py -v -m "performance"                          # Performance tests only
```

## Test Categories

### **1. Unit Tests (18 tests) - Mocked/Isolated**

These tests run quickly and don't require real API keys. They use mocks to simulate external dependencies.

#### **API Key Validation (Tests 1-2)**

- **Test 1:** `test_check_api_keys_valid` - Validates proper API key detection
- **Test 2:** `test_check_api_keys_invalid` - Ensures invalid keys are properly rejected

**Expected Output:**

```
✅ Valid keys return (True, "")
✅ Invalid keys return (False, "error message")
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

#### **Image Processing (Tests 5-6)**

- **Test 5:** `test_prepare_image_valid_pil_image` - PIL image to base64 conversion
- **Test 6:** `test_prepare_image_invalid_input` - Handles non-existent files gracefully

**Expected Output:**

```
✅ Valid images return (True, base64_string)
✅ Invalid inputs return (False, error_message)
```

#### **NVIDIA OCR Unit Tests (Tests 7-9)**

- **Test 7:** `test_nvidia_transcribe_image_success` - Mocked successful NVIDIA API transcription
- **Test 8:** `test_nvidia_transcribe_image_api_failure` - API request failure handling
- **Test 9:** `test_nvidia_transcribe_image_no_api_key` - Missing API key behavior

**Expected Output:**

```
✅ Valid NVIDIA API responses return transcribed text
✅ API failures are handled gracefully with error messages
✅ Missing API keys don't crash the application
```

#### **Frame Processing (Tests 10-11)**

- **Test 10:** `test_process_frame_with_order` - Single frame with order preservation
- **Test 11:** `test_process_video_frames_parallel_success` - Parallel processing integrity

**Expected Output:**

```
✅ Frame order is maintained during processing
✅ Parallel processing returns correct number of results
✅ All frames are processed successfully
```

#### **Gemini Video Processing (Tests 12-13)**

- **Test 12:** `test_process_frames_with_gemini_success` - Mocked Gemini API success
- **Test 13:** `test_process_frames_with_gemini_no_api_key` - API key validation

**Expected Output:**

```
✅ Valid frames return processed content
✅ Missing API key returns appropriate error message
```

#### **Flask Routes (Tests 14-15)**

- **Test 14:** `test_health_check_endpoint` - Health endpoint functionality
- **Test 15:** `test_upload_endpoint_no_file` - Missing file handling

**Expected Output:**

```
✅ /health returns {"status": "healthy"}
✅ Missing file returns 400 error
```

#### **Dependency Management (Tests 16-17)**

- **Test 16:** `test_check_dependencies_valid` - FFmpeg availability check
- **Test 17:** `test_check_dependencies_missing` - Missing dependency handling

**Expected Output:**

```
✅ Available FFmpeg passes validation
✅ Missing FFmpeg raises DependencyError
```

#### **API Retry Logic (Test 18)**

- **Test 18:** `test_make_api_request_success` - Successful API call

**Expected Output:**

```
✅ Successful requests complete on first attempt
```

### **2. Integration Tests (4 tests) - Real APIs**

These tests require valid API keys and make real API calls. They verify end-to-end functionality.

#### **NVIDIA OCR Integration (Test 19)**

- **Test 19:** `test_nvidia_real_api_integration` - Real NVIDIA API integration with test images

**Expected Output:**

```
✅ Real NVIDIA API returns valid string responses
⚠️  Requires valid NVIDIA_API_KEY
```

#### **Gemini API Integration (Tests 20-21)**

- **Test 20:** `test_gemini_integration_real_api` - Full Gemini API integration
- **Test 21:** `test_empty_input_real_api` - Empty input with real API

**Expected Output:**

```
✅ Real Gemini API processes frame texts successfully
✅ Empty input handled appropriately
⚠️  Requires valid GEMINI_API_KEY
```

#### **End-to-End Integration (Test 22)**

- **Test 22:** `test_full_pipeline_real_apis` - Complete pipeline test (NVIDIA OCR → Gemini processing)

**Expected Output:**

```
✅ Full pipeline processes images through both APIs
✅ OCR results flow correctly to Gemini processing
⚠️  Requires both NVIDIA_API_KEY and GEMINI_API_KEY
```

### **3. Performance Tests (Test 23)**

These tests measure system performance and efficiency.

#### **Processing Performance (Test 23)**

- **Test 23:** `test_large_frame_processing_performance` - Large batch processing efficiency

**Expected Output:**

```
✅ 50 frames processed in < 5 seconds
✅ Parallel processing scales appropriately
```

### **4. Edge Case Tests (Tests 24-25)**

These tests verify handling of edge cases and boundary conditions.

#### **Edge Cases (Tests 24-25)**

- **Test 24:** `test_empty_frame_list_processing` - Empty frame list handling
- **Test 25:** `test_single_frame_processing` - Single frame processing

**Expected Output:**

```
✅ Empty frame lists return empty results
✅ Single frames are processed correctly
```

## API Key Setup

To run integration tests, you'll need valid API keys:

### **1. NVIDIA API Key**

1. Visit [NVIDIA Build](https://build.nvidia.com/settings/api-keys)
2. Create an account and generate an API key
3. Set the environment variable:

```bash
# Windows
set NVIDIA_API_KEY=your_nvidia_api_key_here

# Linux/Mac
export NVIDIA_API_KEY=your_nvidia_api_key_here
```

### **2. Google AI Studio API Key**

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Create an account and generate an API key
3. Set the environment variable:

```bash
# Windows
set GEMINI_API_KEY=your_gemini_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_gemini_api_key_here
```

## Running Tests

### **Ultra-Simple Test Runner (Only Way)**

The test runner is zero-configuration:

```bash
python tests/run_tests.py
```

**Features:**

- **Zero Configuration:** No arguments, no flags, no options
- **Runtime:** ~10-15 seconds for all tests
- **Requirements:** Optional API keys for integration tests
- **Coverage:** All 25 tests automatically executed
- **Error Handling:** Clear messages for common issues

**Example Output:**

```
🧪 Running All Tests in test_boardcast.py
============================================================
📊 Total Tests: 25 (18 unit + 4 integration + 1 performance + 2 edge cases)

===== test session starts =====
...
===== 25 passed in 11.41s =====

✅ All tests completed successfully!

📈 Test Coverage:
   • API Integration (NVIDIA OCR + Gemini)
   • Image & Video Processing
   • Error Handling & Edge Cases
   • Performance & Parallel Processing
   • Flask Routes & Dependencies
```

## Test Coverage

The test suite provides comprehensive coverage of:

- ✅ **API Integration** - Both NVIDIA OCR and Gemini APIs
- ✅ **Image Processing** - PIL image handling and base64 conversion
- ✅ **Video Processing** - Frame extraction and parallel processing
- ✅ **Error Handling** - API failures, missing keys, invalid inputs
- ✅ **Performance** - Parallel processing efficiency
- ✅ **Flask Routes** - All application endpoints
- ✅ **Configuration** - API key validation and worker optimization
- ✅ **Dependencies** - System dependency verification
- ✅ **Edge Cases** - Boundary conditions and error states

## Common Issues and Solutions

### **API Key Issues**

```
FAILED tests/test_boardcast.py::TestNVIDIAOCRIntegration::test_nvidia_real_api_integration
SKIPPED [1] NVIDIA integration tests require a valid NVIDIA_API_KEY
```

**Solution:** Set your NVIDIA_API_KEY environment variable.

### **Dependency Issues**

```
FAILED tests/test_boardcast.py::TestDependencyManagement::test_check_dependencies_valid
DependencyError: FFmpeg not found
```

**Solution:** Install FFmpeg on your system.

### **Network Issues**

```
FAILED tests/test_boardcast.py::TestNVIDIAOCRIntegration::test_nvidia_real_api_integration
ConnectionError: Failed to establish connection
```

**Solution:** Check your internet connection and API key validity.

### **Rate Limiting**

```
FAILED tests/test_boardcast.py::TestEndToEndIntegration::test_full_pipeline_real_apis
AssertionError: API request failed: 429 Client Error: Too Many Requests
```

**Solution:** This is normal for integration tests. Wait a moment and try again.

## Test Output Example

```
🧪 Running All Tests (25 total: 18 unit + 4 integration + 1 performance + 2 edge cases)
============================================================

===== test session starts =====
platform win32 -- Python 3.10.0
collecting ...

tests/test_boardcast.py::TestAPIKeyValidation::test_check_api_keys_valid PASSED     [ 4%]
tests/test_boardcast.py::TestAPIKeyValidation::test_check_api_keys_invalid PASSED  [ 8%]
tests/test_boardcast.py::TestWorkerOptimization::test_get_optimal_workers_low_end PASSED [12%]
...
tests/test_boardcast.py::TestEdgeCases::test_single_frame_processing PASSED       [100%]

===== 25 passed in 11.41s =====

✅ All tests completed successfully!
📊 Test Summary:
   • Total Tests: 25 (streamlined from 36)
   • Unit Tests: 18 (mocked dependencies)
   • Integration Tests: 4 (real API calls)
   • Performance Tests: 1 (efficiency validation)
   • Edge Case Tests: 2 (boundary conditions)

```
