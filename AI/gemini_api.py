from vertexai.preview.generative_models import GenerativeModel, Image
import streamlit as st
import vertexai  # Importing Vertex AI SDK
import tempfile  # For creating temporary files and directories
import os  # For interacting with the operating system
from PIL import Image 
import io


# Replace with your Vertex AI project ID
PROJECT_ID = "gen-ai-2024"

# Region where your Vertex AI resources are located
REGION = "us-central1"
# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)

prompt = """
  Analyze this image to find the names of the foods in the image. 
  Write the food item and your estimate for the expiry date for that item when stored appropriately, in an array of objects format.
  Use this example as context: [{"name": "bread", "expiry": 10}, {"name": "apple", "expiry": 8}, {"name": "coffee", "expiry": 16}]
  There are two properties: the name of the item with no adjectives in lowercase, 
  and the number of days before it will go bad when stored appropriately as an integer.
  If no food items are found, return -1.
  """
import requests  # For making HTTP requests
from vertexai.preview.generative_models import Part

def generate_response(image_data):
  """Function to generate response based on an image."""

  # Initialize the GenerativeModel with a specific model
  generative_multimodal_model = GenerativeModel("gemini-1.0-pro-vision-001")

  # Create a Part object with the image data and the content type
  image_part = Part(data=image_data, content_type="image/jpeg")

  # Generate content based on the prompt and image
  response = generative_multimodal_model.generate_content([prompt, image_part])
  
  # Return the generated response
  return response.candidates[0].content.text

def main():
  """Main function for running the Streamlit web application."""

  # Set the title   
  st.title("Vertex AI with Gemini Pro Vision")

  # Allow users to enter an image URL
  image_url = st.text_input("Enter an image URL")

  # If an image URL is entered
  if image_url:
    # Download the image from the URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an exception if the request failed

    # Generate a response based on the image
    response = generate_response(response.content)

    # Display the generated response
    st.header("Answer")
    st.write(response)

# Entry point of the script
if __name__ == "__main__":
  main()