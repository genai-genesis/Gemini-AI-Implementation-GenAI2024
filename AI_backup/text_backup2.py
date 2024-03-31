from vertexai.preview.generative_models import GenerativeModel, Image
from google.cloud import vision
import streamlit as st
import vertexai  # Importing Vertex AI SDK
import tempfile  # For creating temporary files and directories
import os  # For interacting with the operating system

# Replace with your Vertex AI project ID
PROJECT_ID = "gen-ai-2024"

# Region where your Vertex AI resources are located
REGION = "us-central1"
# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Initialize an empty string to store the detected text
    detected_text = ""

    for text in texts:
        # Append the detected text to the string
        detected_text += text.description + " "

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    # Return the detected text as a string
    return detected_text.strip()

def generate_response(receipt_text):
  """Function to generate response based on a receipt text."""

  # Initialize the GenerativeModel with a specific model
  generative_multimodal_model = GenerativeModel("gemini-1.0-pro-vision-001")

  # Fixed text prompt
  prompt = """
  Analyze this text to find the names of the foods in the text. 
  Write the food item and your estimate for the expiry date for that item when stored appropriately, in an array of objects format.
  Use this example as context: [{"name": "bread", "expiry": 10}, {"name": "apple", "expiry": 8}, {"name": "coffee", expiry: 16}]
  There are two properties. the name of the item with no adjectives in lowercase, 
  and the number of days before it will go bad when stored appropriately as an integer.
  """


  # Generate content based on the prompt and receipt text
  response = generative_multimodal_model.generate_content([prompt, receipt_text])

  # Return the generated response
  return response.candidates[0].content.text

def main():
  """Main function for running the Streamlit web application."""

  # Set the title   
  st.title("Vertex AI with Gemini Pro Vision")

  # Allow users to upload an image
  uploaded_file = st.file_uploader("Upload an image")

  # If an image is uploaded
  if uploaded_file is not None:
    # Save the uploaded image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
      temp_file.write(uploaded_file.getvalue())
      temp_path = temp_file.name

    # Detect text from the image
    receipt_text = detect_text(temp_path)

    # Delete the temporary file
    os.remove(temp_path)

    # Generate a response based on the detected text
    response = generate_response(receipt_text)

    # Display the detected text and the generated response
    #st.header("Detected Text")
    #st.write(receipt_text)
    st.header("Receipt Analysis")
    st.write(response)

# Entry point of the script
if __name__ == "__main__":
  main()

# streamlit run gemini_api.py