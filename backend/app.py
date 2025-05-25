from flask import Flask, request, jsonify
from flask_cors import CORS
from process_frames import transcribe_image
from video_utils import extract_frames, tmp_dir
from pathlib import Path
import os

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and transcription requests.
    Supports both image and video files.
    
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
                
                # Process each frame and combine results
                results = []
                for frame in frames:
                    result = transcribe_image(frame)
                    if not result.startswith('API request failed') and not result.startswith('Failed to process'):
                        results.append(result)
                
                return jsonify({'text': '\n'.join(results)})
            else:
                # Process as single image
                result_text = transcribe_image(file_path)
                return jsonify({'text': result_text})

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
