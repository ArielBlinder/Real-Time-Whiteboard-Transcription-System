import unittest
from unittest.mock import patch, Mock, MagicMock, mock_open
import tempfile
import json
import requests
from pathlib import Path
from PIL import Image
import io
import base64
import os

# Import the modules to test
import sys
# Add the parent directory (Backend) to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from process_video_text import process_frames_with_gemini, make_api_request_with_retry, OPENROUTER_API_KEY
from process_frames import prepare_image, transcribe_image, NVIDIA_API_KEY
from video_utils import check_dependencies, extract_frames_to_memory, tmp_dir
from app import check_api_keys, get_optimal_workers, process_frame_with_order, process_video_frames_parallel


class TestProcessVideoText(unittest.TestCase):
    """Test cases for process_video_text.py module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_frame_texts = [
            "Formula: y = mx + b",
            "Where m is the slope",
            "And b is the y-intercept"
        ]
    
    @patch('process_video_text.OPENROUTER_API_KEY', 'test-key')
    @patch('process_video_text.make_api_request_with_retry')
    def test_process_frames_with_gemini_success(self, mock_api_request):
        """Test 1: Successful processing of frame texts with Gemini API"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Processed transcription text"}}]
        }
        mock_api_request.return_value = mock_response
        
        result = process_frames_with_gemini(self.sample_frame_texts)
        
        self.assertEqual(result, "Processed transcription text")
        mock_api_request.assert_called_once()
    
    def test_process_frames_with_gemini_no_api_key(self):
        """Test 2: Error handling when API key is missing"""
        with patch('process_video_text.OPENROUTER_API_KEY', ''):
            with self.assertRaises(ValueError) as context:
                process_frames_with_gemini(self.sample_frame_texts)
            self.assertIn("OPENROUTER_API_KEY", str(context.exception))
    
    def test_process_frames_with_gemini_empty_frames(self):
        """Test 3: Handling empty frame texts list"""
        with patch('process_video_text.OPENROUTER_API_KEY', 'test-key'):
            result = process_frames_with_gemini([])
            self.assertEqual(result, "No frame texts provided for processing")
    
    @patch('requests.post')
    def test_make_api_request_with_retry_success(self, mock_post):
        """Test 4: Successful API request with retry logic"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        headers = {"Authorization": "Bearer test-key"}
        data = {"model": "test-model", "messages": []}
        
        result = make_api_request_with_retry(
            "https://test.api.com", headers, data
        )
        
        self.assertEqual(result, mock_response)
        mock_post.assert_called_once()
    
    @patch('requests.post')
    @patch('time.sleep')
    def test_make_api_request_with_retry_rate_limit(self, mock_sleep, mock_post):
        """Test 5: API request retry logic for rate limiting (429 error)"""
        # First call returns 429, second call succeeds
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        mock_response_success.raise_for_status.return_value = None
        
        mock_post.side_effect = [mock_response_429, mock_response_success]
        
        headers = {"Authorization": "Bearer test-key"}
        data = {"model": "test-model"}
        
        result = make_api_request_with_retry(
            "https://test.api.com", headers, data, max_retries=2
        )
        
        self.assertEqual(result, mock_response_success)
        self.assertEqual(mock_post.call_count, 2)
        mock_sleep.assert_called_once()


class TestProcessFrames(unittest.TestCase):
    """Test cases for process_frames.py module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test image
        self.test_image = Image.new('RGB', (100, 100), color='white')
    
    def test_prepare_image_pil_image(self):
        """Test 6: Image preparation with PIL Image input"""
        success, result = prepare_image(self.test_image)
        
        self.assertTrue(success)
        self.assertIsInstance(result, str)  # Should be base64 string
        
        # Verify it's valid base64
        try:
            base64.b64decode(result)
        except Exception:
            self.fail("Result is not valid base64")
    
    def test_prepare_image_invalid_input(self):
        """Test 7: Image preparation with invalid input"""
        success, result = prepare_image("invalid_image_data")
        
        self.assertFalse(success)
        self.assertIn("Failed to process image", result)
    
    @patch('process_frames.NVIDIA_API_KEY', 'test-nvidia-key')
    @patch('requests.post')
    def test_transcribe_image_success(self, mock_post):
        """Test 8: Successful image transcription"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Transcribed text from image"}}]
        }
        mock_post.return_value = mock_response
        
        result = transcribe_image(self.test_image)
        
        self.assertEqual(result, "Transcribed text from image")
        mock_post.assert_called_once()
    
    @patch('process_frames.NVIDIA_API_KEY', 'test-nvidia-key')
    @patch('requests.post')
    def test_transcribe_image_api_failure(self, mock_post):
        """Test 9: Image transcription API failure handling"""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        result = transcribe_image(self.test_image)
        
        self.assertIn("API request failed", result)


class TestVideoUtils(unittest.TestCase):
    """Test cases for video_utils.py module"""
    
    @patch('subprocess.run')
    def test_check_dependencies_success(self, mock_run):
        """Test 10: Successful dependency check"""
        mock_run.return_value = Mock(returncode=0)
        
        try:
            check_dependencies()
        except Exception:
            self.fail("check_dependencies() raised an exception unexpectedly")
    
    @patch('subprocess.run')
    def test_check_dependencies_missing(self, mock_run):
        """Test 11: Missing dependencies detection"""
        mock_run.side_effect = FileNotFoundError("Command not found")
        
        with self.assertRaises(Exception) as context:
            check_dependencies()
        self.assertIn("Missing system packages", str(context.exception))
    
    def test_tmp_dir_context_manager(self):
        """Test 12: Temporary directory context manager"""
        with tmp_dir() as temp_dir:
            temp_path = Path(temp_dir)
            self.assertTrue(temp_path.exists())
            
            # Create a test file
            test_file = temp_path / "test.txt"
            test_file.write_text("test content")
            self.assertTrue(test_file.exists())
        
        # Directory should be cleaned up after context
        self.assertFalse(temp_path.exists())


class TestApp(unittest.TestCase):
    """Test cases for app.py module"""
    
    def test_check_api_keys_valid(self):
        """Test 13: API key validation with valid keys"""
        with patch('app.NVIDIA_API_KEY', 'valid-nvidia-key'), \
             patch('app.OPENROUTER_API_KEY', 'valid-openrouter-key'):
            
            keys_valid, error_message = check_api_keys()
            
            self.assertTrue(keys_valid)
            self.assertEqual(error_message, "")
    
    def test_check_api_keys_invalid(self):
        """Test 14: API key validation with invalid keys"""
        with patch('app.NVIDIA_API_KEY', 'ADD_KEY_HERE'), \
             patch('app.OPENROUTER_API_KEY', 'ADD_KEY_HERE'):
            
            keys_valid, error_message = check_api_keys()
            
            self.assertFalse(keys_valid)
            self.assertIn("NVIDIA API key not set", error_message)
            self.assertIn("OpenRouter API key not set", error_message)
    
    @patch('os.cpu_count')
    def test_get_optimal_workers_low_end(self, mock_cpu_count):
        """Test 15: Optimal worker calculation for low-end systems"""
        mock_cpu_count.return_value = 2
        
        workers = get_optimal_workers()
        
        self.assertGreaterEqual(workers, 2)
        self.assertLessEqual(workers, 4)
    
    @patch('os.cpu_count')
    def test_get_optimal_workers_high_end(self, mock_cpu_count):
        """Test 16: Optimal worker calculation for high-end systems"""
        mock_cpu_count.return_value = 16
        
        workers = get_optimal_workers()
        
        self.assertGreaterEqual(workers, 2)
        self.assertLessEqual(workers, 20)
    
    def test_process_frame_with_order(self):
        """Test 17: Frame processing with order preservation"""
        with patch('app.transcribe_image') as mock_transcribe:
            mock_transcribe.return_value = "Transcribed text"
            
            frame_data = (5, self.test_image)
            frame_number, result = process_frame_with_order(frame_data)
            
            self.assertEqual(frame_number, 5)
            self.assertEqual(result, "Transcribed text")
    
    @patch('app.get_optimal_workers')
    @patch('app.process_frame_with_order')
    def test_process_video_frames_parallel_empty(self, mock_process, mock_workers):
        """Test 18: Parallel frame processing with empty input"""
        mock_workers.return_value = 4
        
        result = process_video_frames_parallel([])
        
        self.assertEqual(result, [])
    
    @patch('app.get_optimal_workers')
    def test_process_video_frames_parallel_success(self, mock_workers):
        """Test 19: Successful parallel frame processing"""
        mock_workers.return_value = 4
        
        # Create a mock future that will be returned by submit
        mock_future = Mock()
        mock_future.result.return_value = (0, "Transcribed text")
        
        # Create a mock executor
        mock_executor = Mock()
        mock_executor.submit.return_value = mock_future
        
        # Mock the ThreadPoolExecutor to return our mock executor
        with patch('app.ThreadPoolExecutor') as mock_executor_class:
            mock_executor_class.return_value.__enter__ = Mock(return_value=mock_executor)
            mock_executor_class.return_value.__exit__ = Mock(return_value=None)
            
            # Mock as_completed to return our future
            with patch('app.as_completed') as mock_as_completed:
                mock_as_completed.return_value = [mock_future]
                
                frames = [(0, Image.new('RGB', (100, 100)))]
                result = process_video_frames_parallel(frames)
                
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0], "Transcribed text")
    
    def setUp(self):
        """Set up test fixtures for App tests"""
        self.test_image = Image.new('RGB', (100, 100), color='white')


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    @patch('app.NVIDIA_API_KEY', 'test-nvidia-key')
    @patch('app.OPENROUTER_API_KEY', 'test-openrouter-key')
    @patch('requests.post')
    def test_full_image_processing_pipeline(self, mock_post):
        """Test 20: Full pipeline test for image processing"""
        # Mock API responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Complete transcription"}}]
        }
        mock_post.return_value = mock_response
        
        # Test image preparation and transcription
        test_image = Image.new('RGB', (200, 200), color='blue')
        success, b64_result = prepare_image(test_image)
        self.assertTrue(success)
        
        transcription_result = transcribe_image(test_image)
        self.assertEqual(transcription_result, "Complete transcription")


if __name__ == '__main__':
    # Configure test runner
    unittest.main(verbosity=2, buffer=True) 