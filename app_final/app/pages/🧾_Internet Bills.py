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
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests
import time 
import streamlit.components.v1 as components





st.set_page_config(page_title="Internet Bills", page_icon=":earth_americas:")

st.markdown("<h2 style='font-size: 40px; text-align: center;'> Analyze your Internet bills!! </h2>", unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lotti_internet = "https://lottie.host/0801a3ca-b86e-451c-97a1-bbbabb3c120a/bO3TrZnQlz.json"

lottie_json = load_lottieurl(lotti_internet)

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
model_id = "ISP-M1"

# Initialize the DocumentAnalysisClient
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


# load df from csv
# df = pd.read_csv('../files/output_internet.csv')



# Define a function to run the external script
def run_receipt_script():
    csv_file = '../files/output_internet.csv'
    if not os.path.isfile(csv_file):
        # Create an empty DataFrame to store the results
        df = pd.DataFrame(columns=['img_path', 'date', 'amount', 'ISP'])
        df.to_csv(csv_file, index=False)
    else:
        # If the file exists, append the data to the DataFrame
        df = pd.read_csv(csv_file)




    folder_path = "../isp_images/"

    processed_images = set(df['img_path'])

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, filename)
            
            if img_path not in processed_images:
                st_lottie(lottie_json, speed=1, height=200, width=200 , key="initi")
                try:
                    # Analyze the document using the custom model
                    with open(img_path, "rb") as document:
                        poller = document_analysis_client.begin_analyze_document(model_id, document)
                    result = poller.result()
                            # Process the analysis results as before
                    for idx, document in enumerate(result.documents):
                        data = []
                        for name, field in document.fields.items():
                            field_value = field.value if field.value else field.content
                            data.append(field_value)

                        ISP = data[2]
                        date = data[0]
                        amount = data[1]
                        img_path = img_path


                        new_row = {'img_path': img_path, 'date': date, 'amount': amount, 'ISP': ISP}
                        df.loc[len(df)] = new_row
                        
                        processed_images.add(img_path)
                        # save the df as a csv file
                        df.to_csv('../files/output_internet.csv', index=False)

                except Exception as e:
                    print(e)


    


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



# GENERATE INSIGHTS ============================================================

if st.button('Generate Insight'):
    progress_bar = st.progress(0)  # Create a progress bar

    import plotly.express as px

    df = pd.read_csv('../files/output_internet.csv')

    # st.dataframe(df)

    df.loc[df['ISP'].str.contains('mobitel', case=False, na=False), 'ISP'] = 'MOBITEL'

    mask = df['ISP'] == 'MOBITEL'
    df.loc[mask, 'date'] = pd.to_datetime(df.loc[mask, 'date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d').fillna(df['date'])
    df['amount'] = df['amount'].str.replace(',', '', regex=True).astype(float)
    df['year-month'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
    
    # Group by 'year-month' and 'ISP' and calculate the sum of 'amount'
    df2 = df.groupby(['year-month', 'ISP'])['amount'].sum().reset_index()

    # Sort the DataFrame by 'year-month' for a better visualization
    df2 = df2.sort_values(by='year-month')

    # create another df without img_path column
    df3 = df.drop(columns=['img_path', 'date'])

    # reorganize the columns
    df3 = df3[['year-month', 'amount', 'ISP']]

    df3 = df3.sort_values(by='year-month')
    st.dataframe(df3, use_container_width=True)


    color_mapping = {
    'Dialog': '#ff0000',
    'MOBITEL': '#00ff22',
    }


    import plotly.graph_objects as go

    # Create a Figure
    fig = go.Figure()

    # Add traces for each ISP
    for isp, color in color_mapping.items():
        isp_data = df2[df2['ISP'] == isp]
        fig.add_trace(go.Scatter(x=isp_data['year-month'], y=isp_data['amount'], fill='tozeroy', mode='lines', name=isp, line=dict(color=color)))

    # Customize the plot (optional)
    fig.update_layout(
        xaxis_title='Year-Month',
        yaxis_title='Amount',
        title='ISP-wise Expenses Over Time'
    )

# ---------------------------------------------------------------------------------------------
    from plotly.subplots import make_subplots

    # Filter the data for the ISPs you want to display
    selected_isps = ['Dialog', 'MOBITEL']

    fig2 = go.Figure()

    # Create subplots: use 'domain' type for Pie subplot
    fig2 = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    for i, isp in enumerate(selected_isps):
        isp_data = df3[df3['ISP'] == isp]
        fig2.add_trace(go.Pie(labels=isp_data['year-month'], values=isp_data['amount'], name=isp), 1, i + 1)

    # Use `hole` to create a donut-like pie chart
    fig2.update_traces(hole=0.4, hoverinfo="label+percent+name")

    fig2.update_layout(
        autosize=False,
        title_text="ISP-wise Expenses Over Time",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=selected_isps[0], x=0.18, y=0.5, font_size=20, showarrow=False),
                    dict(text=selected_isps[1], x=0.84, y=0.5, font_size=20, showarrow=False)]
    )









    col1, col2 = st.columns(2)


    with col1:
        st.plotly_chart(fig)
    with col2:
        st.plotly_chart(fig2)

