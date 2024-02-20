import streamlit as st
import textwrap
import os
import PIL.Image
from IPython.display import Markdown
import google.generativeai as genai

# Used to securely store your API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAc7Ii4wHf_whau2q--rgjfdht8-I5xhSY'
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        generative_model_name = m.name
        break

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def generate_questions_from_image(image):
    # Display the uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Initialize generative model
    model = genai.GenerativeModel('gemini-pro-vision')
    
    # Generate questions based on the image
    response = model.generate_content(["Prepare 3 questions for the given image", image], stream=True)
    response.resolve()
    
    # Display the generated questions
    st.write(response.text)
    print(response.text)
def main():
    st.title("Image to Questions Generator")
    st.write("Upload an image and get questions generated based on it.")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        img = PIL.Image.open(uploaded_image)
        generate_questions_from_image(img)

if __name__ == "__main__":
    main()
