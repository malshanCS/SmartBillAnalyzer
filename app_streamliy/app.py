#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# In[ ]:


import streamlit as st
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


# In[ ]:


img_path = "../Data/Internet_bills_slt"

# Create a folder to store uploaded images
os.makedirs(img_path, exist_ok=True)




# In[ ]:
st.markdown("""<style>
.css-cio0dv.ea3mdgi1{
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# Upload an image
st.markdown("<h1 style='font-size: 60px; text-align: center;'> Smart Bill Analyzer</h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📈 Upload", "🗃 Insights"])
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])


# In[ ]:


if uploaded_image:
    # Save the uploaded image
    image_path = os.path.join(img_path, uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())
    st.success("Image uploaded and saved!")


# In[ ]:


# Process the image
if st.button("Process"):
    try:
        # Run the process.py script
        subprocess.run(["python", "../code/slt_extracted.py"])
        st.success("Process done!")
    except Exception as e:
        st.error(f"Error during processing: {str(e)}")


# In[ ]:


# Generate insights
if st.button("Generate Insights"):
    
    try:
        # Read the uploaded CSV file
        uploaded_csv = os.path.join("../files", "isp_data.csv")
        df = pd.read_csv(uploaded_csv)
        buffer = BytesIO()
        subprocess.run(["python", "../code/isp_visualization.py"], check=True, stdout=buffer, text=True)
        # Perform data analysis and create a bar plot
        buffer.seek(0)
        plot_data = buffer.read()

        # Display the plot
        st.write("Generated Insights:")
        st.image(plot_data, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating insights: {str(e)}")


# In[ ]:




