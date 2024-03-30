"""A Streamlit app for extracting Image information using latest gemini-vision-pro API """
# Load the libraries

# from dotenv import load_dotenv
# load_dotenv()


import time
import streamlit as st
#import os
from PIL import Image
import google.generativeai as genai


# Configure the Google API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Additional info on the input to generate_content method.

#     ### Input type flexibility

#     While the underlying API strictly expects a `list[glm.Content]` objects, this method
#     will convert the user input into the correct type. The hierarchy of types that can be
#     converted is below. Any of these objects can be passed as an equivalent `dict`.

#     * `Iterable[glm.Content]`
#     * `glm.Content`
#     * `Iterable[glm.Part]`
#     * `glm.Part`
#     * `str`, `Image`, or `glm.Blob`

#     In an `Iterable[glm.Content]` each `content` is a separate message.
#     But note that an `Iterable[glm.Part]` is taken as the parts of a single message.

# GEMINI's RESPONSE IS AMAZING
# Interpretation:
# This code snippet is likely passing three separate pieces of information to the generate_content method of the Gemini model:
# input_: This could be any valid input type accepted by glm.Content, such as a string, an image, or another glm.Content object.
# img[0]: This seems to be accessing the first element of a list or array named img. It's likely an image or some representation of visual data.
# prompt_input: This is likely a string containing a prompt or instruction for the model.
# By enclosing these elements in a list, you are essentially creating an Iterable[glm.Content] object, where each element in the list represents a separate piece of content for the model to process.
# Therefore, the model might be interpreting this input as:
# First message: input_ (content type depends on the actual data)
# Second message: img (likely an image)
# Third message: prompt_input (a text prompt)
# The model would then generate content based on this sequence of messages. The exact nature of the generated content would depend on the specific model and the provided inputs.
# Note: This is just one possible interpretation based on the limited information provided. The actual meaning and behavior might vary depending on the specific context and implementation of the model.
# If you can provide more details about the model and the types of the input variables, I can give you a more precise explanation.







# Function for generating the response
def get_gemini_content( prompt_input, img, input_ ):
    # Instantiate Gemini model
    model = genai.GenerativeModel('gemini-pro-vision') # or gemini-pro
    # gen_config = genai.GenerationConfig(max_output_tokens=2048,temperature=0.0,top_p=0.4,top_k=1)
    # print(input_)
    # print(prompt_input)
    if input_ is not None:
        response = model.generate_content([img, prompt_input, input_])
    #  For debugging image response and safety_settings
    else:
        reponse = model.generate_content([img, prompt_input,"Describe the image"])
    print("Print Generated content,",response)               
    print("Print candidates",response._result)
    return response.text

# Image function for getting data in bytes : Required by Gemini models
def input_img_bytes(uploaded_file):
    if uploaded_file is not None:
        image_data = {
        'mime_type': uploaded_file.type,
        'data': uploaded_file.getvalue()}
        return image_data
    else:
        raise FileNotFoundError("File is not Uploaded...")
    
    
 # For streaming data with streamlit : Words generate word by word
def stream_data_(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

# Streamlit Page Configuration
st.set_page_config(page_title="Document Intelligene Extractor")
st.header("Gemini AI 🤖")
st.text("Upload , Instruct ,  Generate!!!")


input_ = st.text_input("Input Prompt: ",key="input_")
uploaded_file = st.file_uploader("Choose a file to upload...", type = ['jpg','jpeg','png'])
image = ""

if uploaded_file is not None:
    image =  Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


submit = st.button("Generate")

# The input task to perform
system_instruction = """
 You are an expert in analyzing images and answering questions about images.
"""


if submit:
    if uploaded_file is not None:
        image_data = input_img_bytes(uploaded_file)
        response = get_gemini_content(system_instruction, image_data, input_)
        st.subheader("Gemini Response :")
        # st.write(response)
        stream_data = stream_data_(response)
        st.write_stream(stream_data)
    else:
        st.write("Please upload a file to start") 