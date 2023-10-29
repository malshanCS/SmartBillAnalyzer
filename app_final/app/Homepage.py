import streamlit as st
import pandas as pd
import os
import subprocess
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from PIL import Image
# from streamlit_lottie import st_lottie
# from streamlit_lottie import st_lottie_spinner
import requests
import time 
import streamlit.components.v1 as components

st.set_page_config(page_title="Smart Bill Analyzer", page_icon=":money_with_wings:")

st.markdown("<h2 style='font-size: 70px; text-align: center;'> Smart Bill Analyzer </h2>", unsafe_allow_html=True)

from PIL import Image

def resize_image(in_image_path, image_path, max_size=4 * 1024 * 1024):
    # Open the image
    original_image = Image.open(in_image_path)

    # Get the original image dimensions
    original_width, original_height = original_image.size

    # Calculate the new width and height to reduce the size
    new_width = original_width
    new_height = original_height

    # Calculate the number of channels (assuming 8 bits per channel)
    num_channels = len(original_image.getbands())

    while new_width * new_height * num_channels * 8 > max_size:
        new_width = int(new_width * 0.9)
        new_height = int(new_height * 0.9)

    # Resize the image
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

    # Save the resized image
    resized_image.save(image_path)


endpoint = "https://doc-intelli-instance.cognitiveservices.azure.com/"
key = "9b9763750c344a589be05337462b23d8"
model_id = "classifier-1"





st.sidebar.success("select a page above")

st.markdown("<h3 style='font-size: 20px; text-align: center;'> Smart Bill Analyzer is a tool that helps you to analyze your bills and generate insights. </h3>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 20px; text-align: center;'> Get insights about your expediture 💭 </h3>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size: 20px; text-align: center;'> Upload a bill image to get started! </h3>", unsafe_allow_html=True)

uploaded_images = st.file_uploader("Upload images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_images:
    st.success("Images uploaded and saved!")


img_path = "../Data"

receipt_path = "../receipt_images"
isp_path = "../isp_images"
elec_path = "../utility_images"
water_path = "../utility_images"

single_process_image = ""
up_image = None

for i, uploaded_image in enumerate(uploaded_images):
    original_filename = uploaded_image.name
    up_image = uploaded_image
    single_process_image = f"upload_image_{original_filename}.png"
    image_path = os.path.join(img_path, f"upload_image_{original_filename}.png")
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())



st.write(
    """
    <style>
        .stButton {
            background-image: linear-gradient(to right, #00d2ff, #3a7bd5);
            background-color: #00d2ff;
            color: black;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            cursor: pointer;
            border-radius: 8px;
            border: none;
            transition: background-color 0.5s, box-shadow 0.3s;
        }
        .stButton:hover {
            background-color: #327fa8;
            box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
        }
    </style>
""",
    unsafe_allow_html=True,
)



max_size = 4 * 1024 * 1024

coll1, coll2= st.columns(2)

with coll1:  

    if st.button("Single image Process"):

        progress_bar1 = st.progress(0)

        endpoint = "https://doc-intelli-instance.cognitiveservices.azure.com/"
        key = "9b9763750c344a589be05337462b23d8"
        model_id = "classifier-1"

        # Initialize the DocumentAnalysisClient
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        if single_process_image in os.listdir(img_path):
            document_path = os.path.join(img_path, single_process_image)

            # Analyze the specified image using the custom model
            with open(document_path, "rb") as document:
                poller = document_analysis_client.begin_classify_document(
                    model_id, document
                )

            # fill progress bar for 50%
            progress_bar1.progress(50)

            result = poller.result()

            if result.documents:
                doc_type = result.documents[0].doc_type
                # st.markdown(f"Document type for {single_process_image}: {doc_type}")

                if doc_type == "reciept":
                    # Save the receipt image into the "receipt_images" folder
                    receipt_image_path = os.path.join(receipt_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    resize_image(document_path, receipt_image_path,max_size)

                    # fill progress bar for 75%
                    progress_bar1.progress(75)


                elif doc_type == "isp":
                    # Save the ISP image into the "isp_images" folder
                    isp_image_path = os.path.join(isp_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using resize_image function
                    resize_image(document_path, isp_image_path,max_size)
                    
                    progress_bar1.progress(75)

                
                elif doc_type == "electricity_bill":
                    # Save the ISP image into the "isp_images" folder
                    elec_image_path = os.path.join(elec_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    resize_image(document_path, elec_image_path,max_size)
                    progress_bar1.progress(75)


                elif doc_type == 'water_bill':
                    # Save the ISP image into the "isp_images" folder
                    water_image_path = os.path.join(water_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    resize_image(document_path, water_image_path,max_size)
                    progress_bar1.progress(75)




            else:
                st.markdown(f"No document type found for {single_process_image}")

            
        else:
            st.markdown(f"Image '{single_process_image}' not found in the directory.")

        # fill progress bar for 100%
        progress_bar1.progress(100)


with coll2:

    if st.button("Batch Image Process"):
        progress_bar2 = st.progress(0)

        endpoint = "https://doc-intelli-instance.cognitiveservices.azure.com/"
        key = "9b9763750c344a589be05337462b23d8"
        model_id = "classifier-1"
        image_directory = img_path # Replace with the actual path to your images directory

        # Initialize the DocumentAnalysisClient
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        # List all image files in the specified directory
        image_files = [f for f in os.listdir(image_directory) if f.endswith((".jpg", ".png", ".jpeg"))]
        print(image_files)


        total_iterations = len(image_files)
        for i,single_process_image in enumerate(image_files):
            document_path = os.path.join(image_directory, single_process_image)

            # Check if the image already exists in any of the destination folders, if so, skip it
            if (
                os.path.exists(os.path.join(receipt_path, single_process_image)) or
                os.path.exists(os.path.join(isp_path, single_process_image)) or
                os.path.exists(os.path.join(elec_path, single_process_image)) or
                os.path.exists(os.path.join(water_path, single_process_image))
            ):
                # st.markdown(f"Image '{single_process_image}' already exists in one of the destination folders. Skipping...")
                continue


            # Analyze each image using the custom model
            with open(document_path, "rb") as document:
                poller = document_analysis_client.begin_classify_document(model_id, document)

            result = poller.result()

            if result.documents:
                doc_type = result.documents[0].doc_type
                # st.markdown(f"Document type for {single_process_image}: {doc_type}")

    

                if doc_type == "reciept":
                    # Save the receipt image into the "receipt_images" folder
                    receipt_image_path = os.path.join(receipt_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    # img.save(receipt_image_path)
                    resize_image(document_path, receipt_image_path,max_size)
                    progress_bar2.progress(75)


                elif doc_type == "isp":
                    # Save the ISP image into the "isp_images" folder
                    isp_image_path = os.path.join(isp_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    # img.save(isp_image_path)
                    resize_image(document_path, isp_image_path,max_size)
                    progress_bar2.progress(75)
                
                elif doc_type == "electricity_bill":
                    # Save the ISP image into the "isp_images" folder
                    elec_image_path = os.path.join(elec_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    # img.save(elec_image_path)
                    resize_image(document_path, elec_image_path,max_size)

                elif doc_type == 'water_bill':
                    # Save the ISP image into the "isp_images" folder
                    water_image_path = os.path.join(water_path, single_process_image)
                    # Open the image using Pillow
                    # img = Image.open(document_path)

                    # Save the image using Pillow
                    # img.save(water_image_path)
                    resize_image(document_path, water_image_path,max_size)
                    progress_bar2.progress(75)
            else:
                st.markdown(f"No document type found for {single_process_image}")

            progress = (i + 1) / total_iterations
            progress_bar2.progress(progress)

        progress_bar2.progress(100)
        st.success("Batch processing completed.")
        
