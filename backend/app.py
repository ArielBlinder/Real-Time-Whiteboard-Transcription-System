from flask import Flask, request, jsonify
from flask_cors import CORS
from process_frames import transcribe_image, NVIDIA_API_KEY as NVIDIA_API_KEY
from process_video_text import process_frames_with_gemini, GEMINI_API_KEY
from video_utils import extract_frames_to_memory, tmp_dir
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple
import os

app = Flask(__name__)
CORS(app)

def check_api_keys() -> tuple[bool, str]:
    
    # Checks if required API keys are in the code
    
    # Returns true if keys are OK, otherwise returns false and error message
    
    errors = []
    
    if NVIDIA_API_KEY == "ADD_KEY_HERE":
        errors.append("NVIDIA API key not set.\nPlease add your API key in process_frames.py file.\nGet your API key from https://build.nvidia.com/settings/api-keys")
    
    if GEMINI_API_KEY == "ADD_KEY_HERE":
        errors.append("Google AI Studio API key not set.\nPlease add your API key in process_video_text.py file.\nGet your API key from https://aistudio.google.com/apikey")
    
    if errors:
        return False, "\n\n".join(errors)
    
    return True, "" 

def get_optimal_workers() -> int:
    # Parallel processing
    # Calculating the optimal number of workers based on system configuration
    # Returns: int: Optimal number of worker threads
    
    cpu_cores = os.cpu_count() or 4  # Fallback to 4 if detection fails
    
    
    if cpu_cores <= 2:
        # Low-end systems
        optimal_workers = min(4, cpu_cores * 2)
    elif cpu_cores <= 4:
        # Mid-range systems
        optimal_workers = min(8, cpu_cores * 2)
    elif cpu_cores <= 8:
        # High-end systems
        optimal_workers = min(16, cpu_cores * 2)
    else:
        # Very high-end systems
        optimal_workers = min(20, cpu_cores * 1.5)
    
    # Ensure minimum of 2 workers for basic parallelism
    optimal_workers = max(2, int(optimal_workers))
    
    print(f"System optimization: {cpu_cores} CPU Threads detected, using {optimal_workers} workers")
    return optimal_workers

def process_frame_with_order(frame_data: Tuple[int, any, str]) -> Tuple[int, str, str]:
    
    # Process a single frame and return the result with its original order index and timestamp
    # Args:frame_data: Tuple of (frame_number, frame_itself, timestamp_str)  

    # Returns: Tuple of (frame_number, transcribed_text, timestamp_str)
    
    frame_number, frame_image, timestamp_str = frame_data
    transcribed_text = transcribe_image(frame_image)
    return frame_number, transcribed_text, timestamp_str

def process_video_frames_parallel(frames: List[Tuple[int, any, str]], max_workers: int = None) -> List[Tuple[str, str]]:

    # Process video frames in parallel while maintaining chronological order
    
    # Args: "frames": List of (frame_number, frame_itself, timestamp_str) tuples, "max_workers": Maximum number of parallel workers (calculated if None)
        
    # Returns: List of (transcribed_text, timestamp_str) tuples in chronological order

    if not frames:
        return []
    
    # Calculate optimal workers if not specified
    if max_workers is None:
        max_workers = get_optimal_workers()
    
    # For small frame counts, use workers equal to frames
    effective_workers = min(max_workers, len(frames))
    
    print(f"Processing {len(frames)} frames with {effective_workers} parallel workers")
    
    # Process frames in parallel
    results = {}

    with ThreadPoolExecutor(max_workers=effective_workers) as executor:
        # Submit all frames for processing
        # And remember which frame number belongs to which task for matching results back to their order later
        future_to_frame = {
            executor.submit(process_frame_with_order, frame_data): frame_data[0] 
            for frame_data in frames
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_frame):
            try:
                frame_number, transcribed_text, timestamp_str = future.result()
                results[frame_number] = (transcribed_text, timestamp_str)
            except Exception as e:
                frame_number = future_to_frame[future]
                # Log the error of the frame - use the timestamp from the original frame data
                original_frame_data = next(fd for fd in frames if fd[0] == frame_number)
                timestamp_str = original_frame_data[2]
                results[frame_number] = (f"Error processing frame {frame_number}: {str(e)}", timestamp_str)
    
    # Sort results by frame number to maintain chronological order
    sorted_results = [results[i] for i in sorted(results.keys())]
    
    # Filter out failed transcriptions but keep timestamps
    valid_results = []
    for text, timestamp in sorted_results:
        if text and not text.startswith('API request failed') and not text.startswith('Failed to process') and not text.startswith('Error processing'):
            valid_results.append((text, timestamp))
    
    print(f"Successfully processed {len(valid_results)}/{len(frames)} frames")
    return valid_results

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload and transcription requests

    # For videos, processes frames in parallel with NVIDIA API then refines with Gemini
    # For images, processes with NVIDIA API only
    
    # Returns: JSON response containing transcribed text or error message
    
    try:
        # Check API keys before any processing
        keys_valid, error_message = check_api_keys()
        if not keys_valid:
            return jsonify({'error': error_message}), 400

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Create a temporary directory for the uploaded file only
        with tmp_dir() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save the uploaded file temporarily
            file_path = temp_path / file.filename
            file.save(file_path)
            
            # Check if it is a video file
            if file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                try:
                    # Extract frames directly to memory for processing with timestamps
                    frames = extract_frames_to_memory(file_path)
                    
                    if not frames:
                        return jsonify({'error': 'No frames extracted from video'}), 400
                    
                    # Process frames in parallel with auto-optimized worker count
                    frame_data = process_video_frames_parallel(frames)
                    
                    if not frame_data:
                        return jsonify({'error': 'No valid text extracted from video frames'}), 400
                    
                    # Process the combined frame texts with Gemini API
                    try:
                        processed_text = process_frames_with_gemini(frame_data)
                        return jsonify({
                            'text': processed_text,
                            'frames_processed': len(frame_data),
                            'total_frames': len(frames)
                        })
                    except ValueError as e:
                        return jsonify({'error': str(e)}), 500
                    except Exception as e:
                        return jsonify({'error': f'Gemini processing failed: {str(e)}'}), 500
                        
                except RuntimeError as e:
                    return jsonify({'error': f'Video processing failed: {str(e)}'}), 500
                except Exception as e:
                    return jsonify({'error': f'Unexpected video processing error: {str(e)}'}), 500
                    
            else:
                # Process as single image
                result_text = transcribe_image(file_path)
                return jsonify({'text': result_text})

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    

@app.route('/health', methods=['GET'])
def health_check():
    # Health check endpoint
    return jsonify({'status': 'healthy', 'message': 'Video transcription service is running'})

@app.route('/system-info', methods=['GET'])
def system_info():
    # Get system information and current optimization settings
    cpu_cores = os.cpu_count() or 4
    optimal_workers = get_optimal_workers()
    
    return jsonify({
        'cpu_cores': cpu_cores,
        'optimal_workers': optimal_workers,
        'status': 'System optimized for parallel processing'
    })

if __name__ == '__main__': 
    # Run the app on port 5000 and allow for threading for parallel processing
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)