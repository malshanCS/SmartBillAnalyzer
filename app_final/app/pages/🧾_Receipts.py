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
from azure.ai.formrecognizer import FormRecognizerClient
import mimetypes 
import pandas_bokeh




API_KEY = "bca9d94551544cd5ab627108cde053d9"
ENDPOINT = "https://billdata.cognitiveservices.azure.com/"

form_recognizer_client = FormRecognizerClient(ENDPOINT,AzureKeyCredential(API_KEY))

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


st.title("Receipts")

# Define a function to run the external script
def run_receipt_script():
    csv_file = '../files/output_form.csv'
    if not os.path.isfile(csv_file):
        # Create an empty DataFrame to store the results
        df = pd.DataFrame(columns=['img_path', 'bill_type', 'bill_date', 'bill_amount'])
        df.to_csv(csv_file, index=False)
    else:
        # If the file exists, append the data to the DataFrame
        df = pd.read_csv(csv_file)

    folder_path = "../receipt_images/"

    processed_images = set(df['img_path'])

    
    progress_bar = st.progress(0)  # Create a progress bar object
    i = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, filename)

            if i < 100:
                i += 10
                progress_bar.progress(i)  # Progress to 10% done
            if img_path not in processed_images:
                with open(img_path, "rb") as image_file:
                    name = ""
                    total = 0
                    date = ""
                    content_type, _ = mimetypes.guess_type(img_path)

                    poller = form_recognizer_client.begin_recognize_receipts(image_file, content_type=content_type)

                    results = poller.result()

                    for receipt in results:
                        for name, field in receipt.fields.items():
                            if name == 'Total':
                                total = field.value
                            elif name == 'TransactionDate':
                                date = field.value
                            elif name == 'ReceiptType':
                                bill_type = field.value

                    new_row = {'img_path': img_path, 'bill_type': bill_type, 'bill_date': date, 'bill_amount': total}
                    df.loc[len(df)] = new_row
                    processed_images.add(img_path)

    # save the df as a csv file
    df.to_csv('../files/output_form.csv', index=False)
    progress_bar.progress(100)  # Progress to 100% done
                

# Create a button to trigger the script execution
if st.button("Process"):
    
    info_placeholder = st.empty()  # Create an empty placeholder for dynamic text
    info_placeholder.info("Processing receipts...")

    run_receipt_script()
      # Progress to 100% done
    # Replace the message in the placeholder
    info_placeholder.success("Receipts processed and saved!")


# GENERATE INSIGHTS ============================================================

if st.button('Generate Insight'):
    import plotly.express as px

    df = pd.read_csv('../files/output_form.csv')
    # convert bill_date to datetime
    df['bill_date'] = pd.to_datetime(df['bill_date'])
    # Create a new column 'year-month'
    
    df['year-month'] = df['bill_date'].dt.strftime('%Y-%m')
    # st.dataframe(df, use_container_width=True)
    

    # Group by 'year-month' and calculate the sum of 'bill_amount'
    bill_totals_per_year_month = df.groupby('year-month')['bill_amount'].sum().reset_index()
    
    df1 = pd.DataFrame(bill_totals_per_year_month, columns=['year-month', 'bill_amount'])

    # st.dataframe(df1, use_container_width=True)
    # Create a Plotly Table
    import plotly.graph_objects as go
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df1.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df1['year-month'], df1['bill_amount']],
                fill_color='lavender',
                align='left'))
    ])



    # Display the Plotly Table in the Streamlit app
    st.plotly_chart(fig)

    # Create the year-month line graph using Plotly Express
    fig = px.line(df1, x='year-month', y='bill_amount', markers=True)

    df1['year'] = df1['year-month'].str.split('-').str[0]
    df1['month'] = df1['year-month'].str.split('-').str[1]

    # st.dataframe(df1)

    # Customize the plot (optional)
    fig.update_layout(
        title='Year-Month Line Graph',
        xaxis_title='Year-Month',
        yaxis_title='Bill Amount',
        xaxis=dict(
            title_font=dict(size=25),  # Set x-axis title font size
            tickfont=dict(size=14),  # Set x-axis tick label font size
        ),
        yaxis=dict(
            title_font=dict(size=25),  # Set y-axis title font size
            tickfont=dict(size=14),  # Set y-axis tick label font size
        ),
        font=dict(size=32),
        width=400,  # Set the width of the plot
        height=300,  # Set the height of the plot
    )

    df2 = df1[['year','month', 'bill_amount']]
    df2 = df2.rename(columns={'year': 'Year','month':'Month', 'bill_amount': 'Bill Total'})

    # st.dataframe(df2)

    most_recent_years = df2['Year'].unique()[-4:]
    df_most_recent = df2[df2['Year'].isin(most_recent_years)]

    # st.dataframe(df_most_recent)
    

    # Create the area plots
    fig2 = px.area(df_most_recent, x='Month', y='Bill Total', facet_col='Year', facet_col_wrap=1,
                color='Year',  # Use different colors for each year
                labels={'Bill Total': 'Bill Total'},  # Customize the label
                facet_col_spacing=1,  # Adjust the spacing between columns
                facet_row_spacing=0.1
                )  # Set a common title

    # Customize the Y-axis range for each graph
    for year in df_most_recent['Year'].unique():
        fig2.update_yaxes(range=[0, df_most_recent['Bill Total'].max()], row=df_most_recent['Year'].unique().tolist().index(year) + 1)

    fig2.update_layout(
    width=1000,  # Set the width of the plot
    height=800,  # Set the height of the plot
    margin=dict(l=100, r=100, t=30, b=30)
    )




    # Increase font size and center-align text using HTML/CSS
    markdown_text = """
    <h2 style="text-align:center; font-size:30px;">Year-Month Line Graph</h2>
    """

    # Render the Markdown content
    st.markdown(markdown_text, unsafe_allow_html=True)
    fig.update_layout(
    width=1000,  # Set the width of the plot
    height=300,  # Set the height of the plot
    margin=dict(l=100, r=100, t=30, b=30)
    )
    st.plotly_chart(fig)
    # Add custom CSS styles
    st.markdown(
        """
        <style>
        .stApp {
            padding: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
        # Increase font size and center-align text using HTML/CSS
    markdown_text = """
    <h2 style="text-align:center; font-size:30px;">Year Wise Expenditure</h2>
    """

    # Render the Markdown content
    st.markdown(markdown_text, unsafe_allow_html=True)
    st.plotly_chart(fig2)
