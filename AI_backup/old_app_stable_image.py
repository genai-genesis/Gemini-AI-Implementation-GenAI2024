# for gemini_api, first AI model

import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import gemini_api  # Assuming gemini_api.py is in the same directory


app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(error='No selected file'), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join('/tmp', filename)  # Save to /tmp directory
    file.save(filepath)
    try:
        response = gemini_api.generate_response(filepath)
       # response = response.strip('`')  # Remove backticks from the start and end of the string
       # response = ast.literal_eval(response)  # Convert string to list of dictionaries

    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        os.remove(filepath)  # Delete the file after processing
    return response

if __name__ == "__main__":
    app.run(debug=True)
    