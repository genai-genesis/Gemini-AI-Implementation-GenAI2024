from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from vertexai.preview.generative_models import GenerativeModel
import vertexai  # Importing Vertex AI SDK
import os

# Replace with your Vertex AI project ID
PROJECT_ID = "gen-ai-2024"

# Region where your Vertex AI resources are located
REGION = "us-central1"

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)

app = Flask(__name__)

prompt = """
  Using the different food items listed, write a recipe that includes all the items. It is okay 
  to use some additional ingredients to make the recipe work, although the listed items should be 
  the main ingredients.
  """

def generate_response(text_input):
  """Function to generate response based on a text input."""

  # Initialize the GenerativeModel with a specific model
  generative_multimodal_model = GenerativeModel("gemini-1.0-pro-vision-001")

  # Generate content based on the prompt and text input
  response = generative_multimodal_model.generate_content([prompt, text_input])
  
  # Return the generated response
  return response.candidates[0].content.text

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    text_input = request.form.get('text')
    if not text_input:
        return jsonify(error='No text provided'), 400
    try:
        response = generate_response(text_input)
    except Exception as e:
        return jsonify(error=str(e)), 500
    return jsonify(response=response)

if __name__ == "__main__":
    app.run(debug=True)