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
from process_frames import prepare_image, transcribe_image
from process_video_text import process_frames_with_gemini, make_api_request_with_retry, OPENROUTER_API_KEY
from video_utils import check_dependencies, extract_frames_to_memory, DependencyError


# ===============================
# UNIT TESTS (Mocked/Isolated)
# ===============================

class TestAPIKeyValidation:
    """Test API key validation functionality"""
    
    # Test 1: Valid API keys
    @patch('app.NVIDIA_API_KEY', 'valid_nvidia_key')
    @patch('app.OPENROUTER_API_KEY', 'valid_openrouter_key')
    def test_check_api_keys_valid(self):
        """Test that valid API keys pass validation"""
        is_valid, error_msg = check_api_keys()
        assert is_valid is True
        assert error_msg == ""
    
    # Test 2: Invalid API keys
    @patch('app.NVIDIA_API_KEY', 'ADD_KEY_HERE')
    @patch('app.OPENROUTER_API_KEY', 'ADD_KEY_HERE')
    def test_check_api_keys_invalid(self):
        """Test that placeholder API keys fail validation with appropriate error messages"""
        is_valid, error_msg = check_api_keys()
        assert is_valid is False
        assert "NVIDIA API key not set" in error_msg
        assert "OpenRouter API key not set" in error_msg
        assert "https://build.nvidia.com/settings/api-keys" in error_msg


class TestWorkerOptimization:
    """Test worker count optimization logic"""
    
    # Test 3: Low-end system optimization
    @patch('os.cpu_count', return_value=2)
    def test_get_optimal_workers_low_end(self, mock_cpu_count):
        """Test worker optimization for low-end systems (2 cores)"""
        workers = get_optimal_workers()
        assert workers == 4  # min(4, 2*2)
        assert workers >= 2  # Minimum threshold
    
    # Test 4: High-end system optimization
    @patch('os.cpu_count', return_value=16)
    def test_get_optimal_workers_high_end(self, mock_cpu_count):
        """Test worker optimization for high-end systems (16 cores)"""
        workers = get_optimal_workers()
        assert workers == 20  # min(20, 16*1.5) = min(20, 24) = 20
        assert workers >= 2


class TestImageProcessing:
    """Test image preparation and processing functionality"""
    
    # Test 5: Valid image preparation
    def test_prepare_image_valid_pil_image(self):
        """Test successful image preparation with PIL Image object"""
        # Create a test image
        test_image = Image.new('RGB', (100, 100), color='red')
        success, result = prepare_image(test_image)
        
        assert success is True
        assert isinstance(result, str)  # Should be base64 string
        assert len(result) > 0
    
    # Test 6: Invalid image input
    def test_prepare_image_invalid_input(self):
        """Test image preparation with invalid input"""
        success, result = prepare_image("nonexistent_file.jpg")
        assert success is False
        assert "Failed to process image" in result
    
    # Test 7: Large image handling
    def test_prepare_image_large_image(self):
        """Test image preparation correctly resizes large images"""
        # Create a large test image
        large_image = Image.new('RGB', (2000, 2000), color='blue')
        success, result = prepare_image(large_image)
        
        assert success is True
        # Verify the image was processed (base64 encoded)
        assert isinstance(result, str)


class TestFrameProcessing:
    """Test frame processing and transcription functionality"""
    
    # Test 8: Single frame processing with order
    @patch('app.transcribe_image')
    def test_process_frame_with_order(self, mock_transcribe):
        """Test processing a single frame while maintaining order"""
        mock_transcribe.return_value = "Test transcription"
        test_image = Image.new('RGB', (100, 100))
        frame_data = (5, test_image)
        
        frame_number, text = process_frame_with_order(frame_data)
        
        assert frame_number == 5
        assert text == "Test transcription"
        mock_transcribe.assert_called_once_with(test_image)
    
    # Test 9: Parallel frame processing
    @patch('app.transcribe_image')
    def test_process_video_frames_parallel_success(self, mock_transcribe):
        """Test successful parallel processing of multiple frames"""
        mock_transcribe.side_effect = ["Text 1", "Text 2", "Text 3"]
        
        frames = [
            (0, Image.new('RGB', (100, 100))),
            (1, Image.new('RGB', (100, 100))),
            (2, Image.new('RGB', (100, 100)))
        ]
        
        results = process_video_frames_parallel(frames, max_workers=2)
        
        assert len(results) == 3
        assert "Text 1" in results
        assert "Text 2" in results
        assert "Text 3" in results


class TestVideoProcessing:
    """Test video-related processing functionality"""
    
    # Test 10: Gemini processing with valid frames
    @patch('process_video_text.make_api_request_with_retry')
    @patch('process_video_text.OPENROUTER_API_KEY', 'valid_key')
    def test_process_frames_with_gemini_success(self, mock_api_request):
        """Test successful processing of frame texts with Gemini API"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Processed lecture content"}}]
        }
        mock_api_request.return_value = mock_response
        
        frame_texts = ["Math formula 1", "Math formula 2"]
        result = process_frames_with_gemini(frame_texts)
        
        assert result == "Processed lecture content"
        mock_api_request.assert_called_once()
    
    # Test 11: Gemini processing with no API key
    @patch('process_video_text.OPENROUTER_API_KEY', '')
    def test_process_frames_with_gemini_no_api_key(self):
        """Test Gemini processing fails gracefully without API key"""
        frame_texts = ["Some text"]
        
        with pytest.raises(ValueError, match="OPENROUTER_API_KEY environment variable is not set"):
            process_frames_with_gemini(frame_texts)
    
    # Test 12: Empty frame texts handling
    @patch('process_video_text.OPENROUTER_API_KEY', 'valid_key')
    def test_process_frames_with_gemini_empty_frames(self):
        """Test handling of empty frame texts"""
        result = process_frames_with_gemini([])
        assert result == "No frame texts provided for processing"


class TestFlaskRoutes:
    """Test Flask application routes and endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client for Flask app"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    # Test 13: Health check endpoint
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint returns correct status"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'transcription service' in data['message']
    
    # Test 14: System info endpoint
    @patch('app.os.cpu_count', return_value=8)
    def test_system_info_endpoint(self, mock_cpu_count, client):
        """Test system info endpoint returns optimization details"""
        response = client.get('/system-info')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'cpu_cores' in data
        assert 'optimal_workers' in data
        assert data['cpu_cores'] == 8
    
    # Test 15: Upload endpoint with missing file
    @patch('app.check_api_keys', return_value=(True, ''))
    def test_upload_endpoint_no_file(self, mock_keys, client):
        """Test upload endpoint handles missing file gracefully"""
        response = client.post('/upload')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'No file uploaded' in data['error']
    
    # Test 16: Upload endpoint with invalid API keys
    @patch('app.check_api_keys', return_value=(False, 'API keys not set'))
    def test_upload_endpoint_invalid_keys(self, mock_keys, client):
        """Test upload endpoint rejects requests with invalid API keys"""
        # Create a dummy file
        data = {'file': (io.BytesIO(b'dummy content'), 'test.jpg')}
        response = client.post('/upload', data=data)
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'API keys not set' in response_data['error']


class TestDependencyManagement:
    """Test system dependency checking"""
    
    # Test 17: Valid dependencies
    @patch('subprocess.run')
    def test_check_dependencies_valid(self, mock_subprocess):
        """Test successful dependency check when FFmpeg is available"""
        mock_subprocess.return_value = None  # Successful run
        # Should not raise exception
        check_dependencies()
        
        # Verify both ffmpeg and ffprobe were checked
        expected_calls = [
            call(['ffmpeg', '-version'], capture_output=True, check=True),
            call(['ffprobe', '-version'], capture_output=True, check=True)
        ]
        mock_subprocess.assert_has_calls(expected_calls, any_order=True)
    
    # Test 18: Missing dependencies
    @patch('subprocess.run', side_effect=FileNotFoundError())
    def test_check_dependencies_missing(self, mock_subprocess):
        """Test dependency check fails when FFmpeg is missing"""
        with pytest.raises(DependencyError, match="Missing system packages"):
            check_dependencies()


class TestAPIRetryLogic:
    """Test API request retry mechanisms"""
    
    # Test 19: Successful API request without retry
    @patch('requests.post')
    def test_make_api_request_success(self, mock_post):
        """Test successful API request on first attempt"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        url = "https://test.api.com"
        headers = {"Authorization": "Bearer test"}
        data = {"test": "data"}
        
        result = make_api_request_with_retry(url, headers, data)
        assert result == mock_response
        mock_post.assert_called_once()
    
    # Test 20: Rate limiting with retry logic
    @patch('requests.post')
    @patch('time.sleep')
    def test_make_api_request_rate_limit_retry(self, mock_sleep, mock_post):
        """Test API request retry logic handles rate limiting (429 status)"""
        # First call returns 429, second call succeeds
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.raise_for_status.return_value = None
        
        mock_post.side_effect = [mock_response_429, mock_response_200]
        
        url = "https://test.api.com"
        headers = {"Authorization": "Bearer test"}
        data = {"test": "data"}
        
        result = make_api_request_with_retry(url, headers, data, max_retries=3)
        
        assert result == mock_response_200
        assert mock_post.call_count == 2
        mock_sleep.assert_called_once_with(1.0)  # Initial delay


class TestImageTranscription:
    """Test image transcription functionality with API mocking"""
    
    # Test 21: Successful transcription
    @patch('requests.post')
    @patch('process_frames.NVIDIA_API_KEY', 'valid_key')
    def test_transcribe_image_success(self, mock_post):
        """Test successful image transcription with mocked API response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Transcribed text from image"}}]
        }
        mock_post.return_value = mock_response
        
        test_image = Image.new('RGB', (100, 100), color='white')
        result = transcribe_image(test_image)
        
        assert result == "Transcribed text from image"
        mock_post.assert_called_once()


# ===============================
# INTEGRATION TESTS (Real APIs)
# ===============================

@pytest.mark.integration
class TestRealAPIIntegration:
    """Integration tests that use real API calls (requires valid API keys)"""
    
    def setup_method(self):
        """Check if integration tests can run"""
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "ADD_KEY_HERE":
            pytest.skip("Integration tests require a valid OPENROUTER_API_KEY")
    
    # Test 22: Real Gemini API integration
    def test_gemini_integration_real_api(self):
        """Test the Gemini integration with sample OCR data using real API"""
        # Sample OCR texts from multiple frames (simulating video transcription)
        sample_frame_texts = [
            "Mathematical Analysis\nChapter 3: Derivatives",
            "Mathematical Analysis\nChapter 3: Derivatives\n\nDefinition: The derivative of f(x) at point a",
            "Mathematical Analysis\nChapter 3: Derivatives\n\nDefinition: The derivative of f(x) at point a\nf'(a) = lim(h→0) [f(a+h) - f(a)]/h",
            "Mathematical Analysis\nChapter 3: Derivatives\n\nDefinition: The derivative of f(x) at point a\nf'(a) = lim(h→0) [f(a+h) - f(a)]/h\n\nExample: f(x) = x²\nf'(x) = 2x"
        ]
        
        result = process_frames_with_gemini(sample_frame_texts)
        
        # Verify the result is a valid string and contains expected content
        assert isinstance(result, str)
        assert len(result) > 0
        assert not result.startswith("API request failed")
        assert not result.startswith("No valid response")
        
        # The result should be a cleaned version of the mathematical content
        assert "derivative" in result.lower() or "mathematical" in result.lower()
    
    # Test 23: Empty input handling with real API
    def test_empty_input_real_api(self):
        """Test handling of empty input with real API"""
        result = process_frames_with_gemini([])
        assert result == "No frame texts provided for processing"
    
    # Test 24: Invalid input handling with real API
    def test_invalid_input_real_api(self):
        """Test handling of invalid input with real API"""
        result = process_frames_with_gemini(["", "   ", "\n\n"])
        assert result == "No valid text content found in frames"
    
    # Test 25: Single frame processing with real API
    def test_single_frame_real_api(self):
        """Test processing a single frame with real API"""
        frame_texts = ["Simple math equation: 2 + 2 = 4"]
        result = process_frames_with_gemini(frame_texts)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert not result.startswith("API request failed")


# ===============================
# PERFORMANCE TESTS
# ===============================

@pytest.mark.performance
class TestPerformance:
    """Performance-related tests"""
    
    # Test 26: Large frame processing performance
    @patch('app.transcribe_image')
    def test_large_frame_processing_performance(self, mock_transcribe):
        """Test performance with large number of frames"""
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
    
    # Test 27: Worker scaling efficiency
    @patch('app.transcribe_image')
    def test_worker_scaling_efficiency(self, mock_transcribe):
        """Test that more workers improve performance for parallel processing"""
        import time
        
        # Add a small delay to simulate actual work
        def slow_transcribe(*args, **kwargs):
            time.sleep(0.01)  # 10ms delay to simulate API call
            return "Test text"
        
        mock_transcribe.side_effect = slow_transcribe
        frames = [(i, Image.new('RGB', (100, 100))) for i in range(20)]
        
        # Test with 1 worker
        start_time = time.time()
        results_1 = process_video_frames_parallel(frames, max_workers=1)
        time_1_worker = time.time() - start_time
        
        # Test with 4 workers
        start_time = time.time()
        results_4 = process_video_frames_parallel(frames, max_workers=4)
        time_4_workers = time.time() - start_time
        
        # Both should produce the same number of results
        assert len(results_1) == len(results_4) == 20
        
        # With 10ms delay per frame and 20 frames:
        # 1 worker should take ~200ms, 4 workers should take ~50ms
        # Allow for overhead, but 4 workers should be significantly faster for I/O bound tasks
        print(f"1 worker time: {time_1_worker:.3f}s, 4 workers time: {time_4_workers:.3f}s")
        
        # For I/O-bound tasks with sufficient work, more workers should help
        # Allow generous margin for overhead, but expect some improvement
        if time_1_worker > 0.1:  # Only check if there's sufficient work to benefit from parallelization
            assert time_4_workers < time_1_worker * 0.8  # Should be at least 20% faster
        else:
            # For very fast operations, just ensure we don't crash
            assert len(results_4) == 20


if __name__ == "__main__":
    # Run all tests with different markers
    pytest.main([
        __file__, 
        "-v", 
        "-m", "not integration and not performance",  # Run unit tests by default
        "--tb=short"
    ]) 