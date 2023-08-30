#!/usr/bin/env python
# coding: utf-8








import streamlit as st
from streamlit_option_menu import option_menu
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.express as px






img_path = "../Data/batch_process"

# Create a folder to store uploaded images
os.makedirs(img_path, exist_ok=True)



st.markdown("""<style>
.css-cio0dv.ea3mdgi1{
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Upload an image
st.markdown("<h1 style='font-size: 60px; text-align: center;'> Smart Bill Analyzer</h1>", unsafe_allow_html=True)

# Tabs 
selected2 = option_menu(None, ["Home", "Upload", "Insights",], 
    icons=['house', 'cloud-upload', "list-task"],
    menu_icon="cast", default_index=0, orientation="horizontal")








if selected2 == "Home":



    st.markdown("<h2 style='font-size: 30px; text-align: center;'> Home </h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 20px; text-align: center;'> Smart Bill Analyzer is a tool that helps you to analyze your bills and generate insights. </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 20px; text-align: center;'> Upload your bills and generate insights! </h3>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 20px; text-align: center;'> Click on Upload to get started! </h3>", unsafe_allow_html=True)

elif selected2 == "Upload":

    uploaded_images = st.file_uploader("Upload images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)





    # if uploaded_image:
    #     # Save the uploaded image
    #     image_path = os.path.join(img_path, uploaded_image.name)
    #     with open(image_path, "wb") as f:
    #         f.write(uploaded_image.read())

    if uploaded_images:
        st.success("Images uploaded and saved!")

    for i, uploaded_image in enumerate(uploaded_images):
        image_path = os.path.join(img_path, f"uploaded_image_{i}.png")
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())


elif selected2 == "Insights":



    # Process the image
    if st.button("Process"):
        try:
            # Run the process.py script
            subprocess.run(["python", "../code/process.py"])
            st.success("Process done!")
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")





    # Generate insights
    if st.button("Generate Insights"):
        df = pd.read_csv("../files/isp_data_2.csv")

        # Use st.sidebar for select boxes
        x_axis_val = st.sidebar.selectbox("Select the x-axis value", options=df.columns)
        y_axis_val = st.sidebar.selectbox("Select the y-axis value", options=df.columns)

        # Use a separate button to generate the plot
        if st.button("Generate Plot"):
            try:
                if x_axis_val and y_axis_val:  # Check if both axes have been selected
                    plot = px.scatter(df, x=x_axis_val, y=y_axis_val, color="ISP")
                    st.plotly_chart(plot)

            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")

                







