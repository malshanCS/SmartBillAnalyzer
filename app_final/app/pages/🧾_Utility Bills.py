import streamlit as st
from streamlit_option_menu import option_menu
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import json
from azure.core.exceptions import ResourceNotFoundError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import mimetypes 
import pandas_bokeh
from Homepage import session_state


st.set_page_config(page_title="Utility Bills", page_icon="⚡")

st.markdown("<h2 style='font-size: 40px; text-align: center;'> Analyze your Utility bills!! </h2>", unsafe_allow_html=True)

st.write(
    """<style>
    .stButton {
        background-image: linear-gradient(to right, #00d2ff, #3a7bd5);
        color: black;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        border-radius: 8px;
        border: none;
        transition: background-color 0.5s;
    }
    .stButton:hover {
        background-color: #327fa8;
    }
    </style>""",
    unsafe_allow_html=True,
)




endpoint = "https://thilakna-doc-intelligence-instance.cognitiveservices.azure.com/"
key = "29579bf5af1f4559bb8228d643e79d7b"
model_id = "Bills-1"

# Initialize the DocumentAnalysisClient
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)




def run_receipt_script():
    csv_file = '../files/output_utility.csv'
    if not os.path.isfile(csv_file):
        # Create an empty DataFrame to store the results
        df = pd.DataFrame(columns=["img_path","date", "amount", "type"])
        df.to_csv(csv_file, index=False)
    else:
        # If the file exists, append the data to the DataFrame
        df = pd.read_csv(csv_file)


    folder_path = "../utility_images/"

    processed_images = set(df['img_path'])

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, filename)
            
            if img_path not in processed_images:
                # Analyze the document using the custom model
                with open(img_path, "rb") as document:
                    poller = document_analysis_client.begin_analyze_document(
                        model_id, document
                    )

                result = poller.result()

                for idx, document in enumerate(result.documents):
                    data = []
                    for name, field in document.fields.items():
                        field_value = field.value if field.value else field.content
                        data.append(field_value)

                    img_path = img_path
                    date = data[0]
                    amount = data[1]
                    type = data[2]

                    new_row = {
                        "img_path": img_path,
                        "date": date,
                        "amount": amount,
                        "type": type,
                    }

                    df.loc[len(df)] = new_row

                    processed_images.add(img_path)

                    df.to_csv('../files/output_utility.csv', index=False)


                
# Create a button to trigger the script execution
if st.button("Process"):
    progress_bar = st.progress(0)  # Create a progress bar
    info_placeholder = st.empty()  # Create an empty placeholder for dynamic text
    info_placeholder.info("Processing receipts...")

    run_receipt_script()

    # Update the progress bar to 100%
    progress_bar.progress(100)
    # Replace the message in the placeholder
    info_placeholder.success("Receipts processed and saved!")



if st.button('Generate Insights'):
    from Homepage import session_state
    import re
    df = pd.read_csv('../files/output_utility.csv')



    # Function to clean and convert the date values
    def clean_and_convert_date(date_str):
        # date_str = re.sub(r'[^0-9/]', '', date_str)  # Remove non-numeric characters
        date_formats = ['%Y/%m/%d', '%d/%m/%Y', '%d/%m', '%d-%m-%Y']
        for format in date_formats:
            try:
                return pd.to_datetime(date_str, format=format).strftime('%Y-%m')
            except ValueError:
                pass
        return "unknown"
        
    
    df['year-month'] = df['date'].apply(clean_and_convert_date)

    # fill unknown values with 2023-row number
    # df['year-month'] = df['year-month'].replace('unknown', '2023-'+f"{df.index}")
    

    # replace all punctuations in amount column with .
    df['amount'] = df['amount'].str.replace(',', '.')
    df['amount'] = df['amount'].str.replace('-', '.')
    df['amount'] = df['amount'].str.replace(' ', '')

    def replace_second_dot(text):
        return text.replace('..', '.')

    # if there are two . replace the second one with empty
    df['amount'] = df['amount'].apply(replace_second_dot)

    # convert amount column to float
    df['amount'] = df['amount'].astype(float)

    # get type wise sum of amount
    df = df.groupby(['type', 'year-month']).sum().reset_index()

    # replace electricity with Electricity
    df['type'] = df['type'].replace('electricity', 'Electricity')

    df['type'] = df['type'].replace('water', 'Water')

    st.dataframe(df, use_container_width=True)

    # draw a pie chart
    fig = px.pie(df, values='amount', names='type', title='Utility Bills')
    st.plotly_chart(fig, use_container_width=True)

    # draw a bar chart
    fig = px.bar(df, x='year-month', y='amount', color='type', title='Utility Bills')
    st.plotly_chart(fig, use_container_width=True)








