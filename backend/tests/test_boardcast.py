import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
from PIL import Image
import io
import base64
import requests

# Import the modules to test
import sys
sys.path.append('..')
from app import (
    app, check_api_keys, get_optimal_workers, 
    process_frame_with_order, process_video_frames_parallel
)
from process_frames import prepare_image, transcribe_image, NVIDIA_API_KEY
from process_video_text import process_frames_with_gemini, make_api_request_with_retry, GEMINI_API_KEY
from video_utils import check_dependencies, extract_frames_to_memory, DependencyError

# UNIT TESTS 

class TestAPIKeyValidation:
    # Test API key validation functionality
    
    # Test 1: Valid API keys
    @patch('app.NVIDIA_API_KEY', 'valid_nvidia_key')
    @patch('app.GEMINI_API_KEY', 'valid_gemini_key')
    def test_check_api_keys_valid(self):
        # Test that valid API keys pass validation
        is_valid, error_msg = check_api_keys()
        assert is_valid is True
        assert error_msg == ""
    
    # Test 2: Invalid API keys
    @patch('app.NVIDIA_API_KEY', 'ADD_KEY_HERE')
    @patch('app.GEMINI_API_KEY', 'ADD_KEY_HERE')
    def test_check_api_keys_invalid(self):
        # Test that placeholder API keys fail validation with appropriate error messages
        is_valid, error_msg = check_api_keys()
        assert is_valid is False
        assert "NVIDIA API key not set" in error_msg
        assert "Google AI Studio API key not set" in error_msg


class TestWorkerOptimization:
    # Test worker count optimization logic
    
    # Test 3: Low-end system optimization
    @patch('os.cpu_count', return_value=2)
    def test_get_optimal_workers_low_end(self, mock_cpu_count):
        # Test worker optimization for low-end systems - 2 cores
        workers = get_optimal_workers()
        assert workers == 4  # min(4, 2*2)
        assert workers >= 2  # Minimum threshold
    
    # Test 4: High-end system optimization
    @patch('os.cpu_count', return_value=16)
    def test_get_optimal_workers_high_end(self, mock_cpu_count):
        # Test worker optimization for high-end systems - 16 cores
        workers = get_optimal_workers()
        assert workers == 20  # min(20, 16*1.5) = min(20, 24) = 20
        assert workers >= 2


class TestImageProcessing:
    # Test image preparation and processing functionality
    
    # Test 5: Valid image preparation
    def test_prepare_image_valid_pil_image(self):
        # Test successful image preparation with PIL Image object
        test_image = Image.new('RGB', (100, 100), color='red')
        success, result = prepare_image(test_image)
        
        assert success is True
        assert isinstance(result, str)  # Should be base64 string
        assert len(result) > 0
    
    # Test 6: Invalid image input
    def test_prepare_image_invalid_input(self):
        # Test image preparation with invalid input
        success, result = prepare_image("nonexistent_file.jpg")
        assert success is False
        assert "Failed to process image" in result


class TestNVIDIAOCRUnit:
    # Test NVIDIA OCR functionality with mocked API calls
    
    # Test 7: Successful NVIDIA OCR transcription (mocked)
    @patch('requests.post')
    @patch('process_frames.NVIDIA_API_KEY', 'valid_nvidia_key')
    def test_nvidia_transcribe_image_success(self, mock_post):
        # Test successful image transcription with mocked NVIDIA API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "2x + 3 = 7\nSolve for x"}}]
        }
        mock_post.return_value = mock_response
        
        test_image = Image.new('RGB', (100, 100), color='white')
        result = transcribe_image(test_image)
        
        assert result == "2x + 3 = 7\nSolve for x"
        mock_post.assert_called_once()
    
    # Test 8: NVIDIA API request failure
    @patch('requests.post')
    @patch('process_frames.NVIDIA_API_KEY', 'valid_nvidia_key')
    def test_nvidia_transcribe_image_api_failure(self, mock_post):
        # Test NVIDIA OCR handling when API request fails
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        
        test_image = Image.new('RGB', (100, 100), color='white')
        result = transcribe_image(test_image)
        
        assert "API request failed" in result
        assert "Connection error" in result
    
    # Test 9: NVIDIA API with no API key
    @patch('process_frames.NVIDIA_API_KEY', 'ADD_KEY_HERE')
    def test_nvidia_transcribe_image_no_api_key(self):
        # Test NVIDIA OCR behavior when API key is not set
        test_image = Image.new('RGB', (100, 100), color='white')
        result = transcribe_image(test_image)
        # With invalid API key, we expect an API request failure
        assert isinstance(result, str)


class TestFrameProcessing:
    # Test frame processing and transcription functionality
    
    # Test 10: Single frame processing with order
    @patch('app.transcribe_image')
    def test_process_frame_with_order(self, mock_transcribe):
        # Test processing a single frame while maintaining order
        mock_transcribe.return_value = "Test transcription"
        test_image = Image.new('RGB', (100, 100))
        frame_data = (5, test_image)
        
        frame_number, text = process_frame_with_order(frame_data)
        
        assert frame_number == 5
        assert text == "Test transcription"
        mock_transcribe.assert_called_once_with(test_image)
    
    # Test 11: Parallel frame processing
    @patch('app.transcribe_image')
    def test_process_video_frames_parallel_success(self, mock_transcribe):
        # Test successful parallel processing of multiple frames
        mock_transcribe.return_value = "Test text"
        
        frames = [(i, Image.new('RGB', (100, 100))) for i in range(5)]
        results = process_video_frames_parallel(frames, max_workers=2)
        
        assert len(results) == 5
        # All results should be valid text
        for text in results:
            assert text == "Test text"


class TestVideoProcessing:
    # Test video processing with Gemini API
    
    # Test 12: Gemini processing success
    @patch('process_video_text.make_api_request_with_retry')
    @patch('process_video_text.GEMINI_API_KEY', 'valid_key')
    def test_process_frames_with_gemini_success(self, mock_api_request):
        # Test successful processing of frame texts with Gemini API
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Cleaned and organized transcription text"}}]
        }
        mock_api_request.return_value = mock_response
        
        frame_texts = ["Text from frame 1", "Text from frame 2"]
        result = process_frames_with_gemini(frame_texts)
        
        assert result == "Cleaned and organized transcription text"
        mock_api_request.assert_called_once()
    
    # Test 13: Gemini processing without API key
    @patch('process_video_text.GEMINI_API_KEY', '')
    def test_process_frames_with_gemini_no_api_key(self):
        # Test Gemini processing fails gracefully without API key
        frame_texts = ["Sample text"]
        
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
            process_frames_with_gemini(frame_texts)


class TestFlaskRoutes:
    # Test Flask application endpoints
    
    @pytest.fixture
    def client(self):
        # Create test client for Flask app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    # Test 14: Health check endpoint
    def test_health_check_endpoint(self, client):
        # Test the health check endpoint returns correct status
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['message'] == 'Video transcription service is running'
    
    # Test 15: Upload endpoint with no file
    @patch('app.check_api_keys', return_value=(True, ''))
    def test_upload_endpoint_no_file(self, mock_keys, client):
        # Test upload endpoint handles missing file gracefully
        response = client.post('/upload')
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert data['error'] == 'No file uploaded'


class TestDependencyManagement:
    # Test system dependency checks
    
    # Test 16: Valid dependencies
    @patch('subprocess.run')
    def test_check_dependencies_valid(self, mock_subprocess):
        # Test successful dependency check when FFmpeg is available
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "ffmpeg version 4.4.0"
        mock_subprocess.return_value = mock_result
        
        try:
            check_dependencies()
            # Should not raise an exception
            assert True
        except DependencyError:
            assert False, "Should not raise DependencyError when FFmpeg is available"
    
    # Test 17: Missing dependencies
    @patch('subprocess.run', side_effect=FileNotFoundError())
    def test_check_dependencies_missing(self, mock_subprocess):
        # Test dependency check fails when FFmpeg is missing
        with pytest.raises(DependencyError) as exc_info:
            check_dependencies()
        assert "Missing system packages" in str(exc_info.value)


class TestAPIRetryLogic:
    # Test API retry mechanism
    
    # Test 18: Successful API request
    @patch('requests.post')
    def test_make_api_request_success(self, mock_post):
        # Test successful API request on first attempt
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"choices": [{"message": {"content": "Success"}}]}
        mock_post.return_value = mock_response
        
        url = "https://api.example.com/test"
        headers = {"Authorization": "Bearer test"}
        data = {"model": "test", "messages": []}
        
        result = make_api_request_with_retry(url, headers, data)
        
        assert result.json() == {"choices": [{"message": {"content": "Success"}}]}
        mock_post.assert_called_once()

# INTEGRATION TESTS

@pytest.mark.integration
class TestNVIDIAOCRIntegration:
    # Integration tests for NVIDIA OCR with real API calls
    
    def setup_method(self):
        # Check if NVIDIA integration tests can run
        if not NVIDIA_API_KEY or NVIDIA_API_KEY == "ADD_KEY_HERE":
            pytest.skip("NVIDIA integration tests require a valid NVIDIA_API_KEY")
    
    # Test 19: Real NVIDIA API integration
    def test_nvidia_real_api_integration(self):
        # Test NVIDIA OCR integration with a real API call
        test_image = Image.new('RGB', (200, 100), color='white')
        result = transcribe_image(test_image)
        
        assert isinstance(result, str)
        assert not result.startswith("API request failed")


@pytest.mark.integration  
class TestGeminiIntegration:
    # Integration tests for Gemini API with real API calls
    
    def setup_method(self):
        # Check if Gemini integration tests can run
        if not GEMINI_API_KEY or GEMINI_API_KEY == "ADD_KEY_HERE":
            pytest.skip("Gemini integration tests require a valid GEMINI_API_KEY")
    
    # Test 20: Real Gemini API integration
    def test_gemini_integration_real_api(self):
        # Test the Gemini integration with sample OCR data using real API
        sample_frame_texts = [
            "Mathematical Analysis\nChapter 3: Derivatives",
            "Definition: The derivative of f(x) at point a\nf'(a) = lim(h→0) [f(a+h) - f(a)]/h"
        ]
        
        result = process_frames_with_gemini(sample_frame_texts)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert not result.startswith("API request failed")
    
    # Test 21: Empty input handling with real API
    def test_empty_input_real_api(self):
        # Test handling of empty input with real API
        result = process_frames_with_gemini([])
        assert result == "No frame texts provided for processing"


@pytest.mark.integration
class TestEndToEndIntegration:
    # End-to-end integration tests combining NVIDIA OCR and Gemini processing
    
    def setup_method(self):
        # Check if end-to-end integration tests can run
        if not NVIDIA_API_KEY or NVIDIA_API_KEY == "ADD_KEY_HERE":
            pytest.skip("End-to-end tests require a valid NVIDIA_API_KEY")
        if not GEMINI_API_KEY or GEMINI_API_KEY == "ADD_KEY_HERE":
            pytest.skip("End-to-end tests require a valid GEMINI_API_KEY")
    
    # Test 22: Full pipeline test (NVIDIA OCR + Gemini processing)
    def test_full_pipeline_real_apis(self):
        # Test the complete pipeline: NVIDIA OCR -> Gemini processing
        test_images = [
            Image.new('RGB', (200, 100), color='white'),
            Image.new('RGB', (200, 100), color='lightgray')
        ]
        
        # Step 1: Process images with NVIDIA OCR
        ocr_results = []
        for img in test_images:
            result = transcribe_image(img)
            if result and not result.startswith("API request failed"):
                ocr_results.append(result)
        
        # Step 2: Process OCR results with Gemini (if we have valid OCR output)
        if ocr_results:
            final_result = process_frames_with_gemini(ocr_results)
            assert isinstance(final_result, str)
            assert not final_result.startswith("API request failed")
        else:
            # If no valid OCR results, test with placeholder text
            placeholder_texts = ["Sample mathematical content for testing"]
            final_result = process_frames_with_gemini(placeholder_texts)
            assert isinstance(final_result, str)
            assert len(final_result) > 0

# PERFORMANCE TESTS

@pytest.mark.performance
class TestPerformance:
    # Performance-related tests
    
    # Test 23: Large frame processing performance
    @patch('app.transcribe_image')
    def test_large_frame_processing_performance(self, mock_transcribe):
        # Test performance with large number of frames
        import time
        
        mock_transcribe.return_value = "Test text"
        
        # Create 50 frames
        frames = [(i, Image.new('RGB', (100, 100))) for i in range(50)]
        
        start_time = time.time()
        results = process_video_frames_parallel(frames, max_workers=4)
        end_time = time.time()
        
        # Should complete within reasonable time (less than 5 seconds for 50 frames)
        assert end_time - start_time < 5.0
        assert len(results) == 50

# EDGE CASE TESTS

class TestEdgeCases:
    # Test edge cases and error conditions
    
    # Test 24: Empty frame list processing
    def test_empty_frame_list_processing(self):
        # Test processing empty frame list
        results = process_video_frames_parallel([], max_workers=2)
        assert results == []
    
    # Test 25: Single frame processing
    @patch('app.transcribe_image')
    def test_single_frame_processing(self, mock_transcribe):
        # Test processing a single frame
        mock_transcribe.return_value = "Single frame text"
        
        frames = [(0, Image.new('RGB', (100, 100)))]
        results = process_video_frames_parallel(frames, max_workers=2)
        
        assert len(results) == 1
        assert results[0] == "Single frame text"


if __name__ == "__main__":
    # Run all tests with different markers
    pytest.main([
        __file__, 
        "-v", 
        "-m", "not integration and not performance",  # Run unit tests by default
        "--tb=short"
    ]) 