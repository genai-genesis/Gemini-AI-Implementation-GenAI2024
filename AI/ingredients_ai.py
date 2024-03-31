from vertexai.preview.generative_models import GenerativeModel, Image
import streamlit as st
import vertexai  # Importing Vertex AI SDK

# Replace with your Vertex AI project ID
PROJECT_ID = "gen-ai-2024"

# Region where your Vertex AI resources are located
REGION = "us-central1"
# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)


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

def main():
  """Main function for running the Streamlit web application."""

  # Set the title   
  st.title("Vertex AI with Gemini Pro Vision")

  # Allow users to input text
  user_input = st.text_input("Enter your text")

  # If text is input
  if user_input:
    # Generate a response based on the text input
    response = generate_response(user_input)

    # Display the generated response
    st.header("Answer")
    st.write(response)

# Entry point of the script
if __name__ == "__main__":
  main()