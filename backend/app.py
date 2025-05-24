from flask import Flask, request, jsonify
from flask_cors import CORS
from process_frames import transcribe_image

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and transcription requests.
    
    Returns:
        JSON response containing transcribed text or error message
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        result_text = transcribe_image(file)
        return jsonify({'text': result_text})

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)





