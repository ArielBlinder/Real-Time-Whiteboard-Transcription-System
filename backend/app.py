from flask import Flask, request, jsonify
from flask_cors import CORS
from process_frames import transcribe_image
from process_video_text import process_frames_with_gemini
from video_utils import extract_frames, tmp_dir
from pathlib import Path
import os
import concurrent.futures

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and transcription requests.
    Supports both image and video files.
    For videos, processes frames with NVIDIA API then refines with Gemini.
    
    Returns:
        JSON response containing transcribed text or error message
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Create a temporary directory for processing
        with tmp_dir() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save the uploaded file
            file_path = temp_path / file.filename
            file.save(file_path)
            
            # Check if it's a video file
            if file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                # Extract frames from video
                frames = extract_frames(file_path, temp_path)
                if not frames:
                    return jsonify({'error': 'No frames extracted from video'}), 400
                
                # Process each frame with NVIDIA API in parallel while maintaining order
                frame_texts = []
                futures = []
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Submit all frame transcription tasks and store futures in order
                    for frame_path in frames:
                        futures.append(executor.submit(transcribe_image, frame_path))
                    
                    # Retrieve results in the order of submission
                    for i, future in enumerate(futures):
                        try:
                            result = future.result()
                            # Check if the result is valid (not an error message and not empty)
                            if result and not result.startswith('API request failed') and not result.startswith('Failed to process'):
                                frame_texts.append(result)
                            else:
                                frame_texts.append("") # Append empty string for failed/invalid/empty transcription
                                print(f'Frame {i+1} transcription failed or returned: {result}')
                        except Exception as exc:
                            print(f'Frame {i+1} generated an exception during transcription: {exc}')
                            frame_texts.append("") # Append empty string on exception
                
                successfully_processed_count = sum(1 for text in frame_texts if text.strip())

                if successfully_processed_count == 0 and frames: # Check if all transcriptions failed or were empty
                    return jsonify({'error': 'No valid text extracted from video frames after parallel processing'}), 400
                
                # Process the combined frame texts with Gemini API
                try:
                    processed_text = process_frames_with_gemini(frame_texts) # frame_texts now includes empty strings for failed ones
                    return jsonify({
                        'text': processed_text,
                        'frames_processed': successfully_processed_count,
                        'total_frames': len(frames)
                    })
                except ValueError as e:
                    return jsonify({'error': str(e)}), 500
                except Exception as e:
                    return jsonify({'error': f'Gemini processing failed: {str(e)}'}), 500
                    
            else:
                # Process as single image
                result_text = transcribe_image(file_path)
                return jsonify({'text': result_text})

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Video transcription service is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
