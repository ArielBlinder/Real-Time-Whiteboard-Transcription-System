
from flask import Flask, request, jsonify
from flask_cors import CORS
from nv_model import transcribe_image  # <- import our function

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    result_text = transcribe_image(file)
    #result_text = "this is generated"   for check
    return jsonify({'text': result_text})

if __name__ == '__main__':
    app.run(debug=True)





