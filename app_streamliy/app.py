#!/usr/bin/env python
# coding: utf-8








import streamlit as st
from streamlit_option_menu import option_menu
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime




st.set_page_config(page_title="Smart Bill Analyzer", page_icon=":money_with_wings:")


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
        original_filename = uploaded_image.name

        image_path = os.path.join(img_path, f"upload_image_{original_filename}.png")
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())


elif selected2 == "Insights":


    button_style = """
    <style>
        .centered {
            display: flex;
            justify-content: center;
        }
        .stButton>button {
            background-color: #0c7d21;  /* Green */
            color: white;
            width: 100%;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #0f5c01;  /* Darker green on hover */
            color: black;
        }
    </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)
    ###



    # Process the image fds
    if st.button("Process"):
        try:
            # Run the process.py script
            subprocess.run(["python", "../code/process.py"])
            st.success("Process done!")
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")






    # Generate insights
    if st.button("Generate Insights"):

################################################################# Dataframe preparation #################################################################
        isp_data = pd.read_csv('../files/isp_data_2.csv')
        isp_data['date'].fillna('unknown', inplace=True)

        df = isp_data.copy()

        # Filter out rows with "unknown" dates
        df = df[df['date'] != 'unknown']

        # Convert the 'date' column to strings
        df['date'] = df['date'].astype(str)

        # Define a function to clean and fix dates
        def clean_and_fix_dates(date_str):
            try:
                # Check for NaN and convert to "unknown"
                if pd.isna(date_str):
                    return "unknown"
                
                # Try to parse the date
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                # If it's an invalid date, set the month to 12 (December) and day to 31
                date_obj = datetime.strptime(date_str[:4] + '-12-31', '%Y-%m-%d')
            
            return date_obj.strftime('%Y-%m-%d')

        # Apply the function to the 'date' column
        df['date'] = df['date'].apply(clean_and_fix_dates)

        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        #

        monthly_payments = df.groupby(['ISP','year', 'month'])['amount'].sum().reset_index()

        monthly_payments = pd.DataFrame(monthly_payments)

        orig = df.copy()
        df = monthly_payments.copy()
        df['year-month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
        import calendar
        df['date'] = df['year'].astype(str) + '-' + df['month'].apply(lambda x: calendar.month_name[x])


        # Display the DataFrame in Streamlit with some styling
        st.title("Your Internet Expenses!!")

        show_df = df[['date','ISP', 'amount']]
        st.dataframe(show_df, use_container_width=True)




################################################################# Plots #################################################################

        import plotly.graph_objs as go
        import plotly.express as px
        import plotly.subplots as sp

        # # Assuming you have the 'year' and 'month' columns
        # # If not, you can use df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str) to create a 'year-month' column


        # # fig = sp.make_subplots(rows=1, cols=2)

        # # Create a line graph using Plotly
        # trace1 = go.Figure()

        # # Add a line trace for each ISP
        # for isp in df['ISP'].unique():
        #     df_filtered = df[df['ISP'] == isp]
        #     trace1.add_trace(go.Scatter(x=df_filtered['year'].astype(str) + '-' + df_filtered['month'].astype(str),
        #                             y=df_filtered['amount'],
        #                             mode='lines+markers',
        #                             name=isp))

        # # Customize the layout
        # trace1.update_layout(
        #     title='Monthly Expenditure on Internet Services by ISP (Line Graph)',
        #     xaxis_title='Year-Month',
        #     yaxis_title='Amount',
        #     xaxis=dict(tickangle=45),
        #     template="plotly_dark",
        #     width=800,
        #     height=500
        # )


        # Define custom colors for ISPs
        colors = {'Dialog': 'red', 'SLT': 'blue'}

        # Create a bar plot using Plotly Express with custom colors
        trace1 = px.bar(df, x="year-month", y="amount",
                        color="ISP",
                        color_discrete_map=colors,  # Custom colors for ISPs
                        labels={"year-month": "Year & Month", "amount": "Amount"},
                        title="Monthly Expenditure on Internet Services by ISP")
        

        trace1.update_layout(
        title={
            'text': "Monthly Expenditure on Internet Services by ISP",
            'x': 0.5,  # Title position (centered)
            'xanchor': 'center',  # Title anchor point
            'y': 0.95,  # Title Y position
            'yanchor': 'top',  # Title Y anchor point
            'font': {'size': 24}  # Adjust the font size as needed
        }
)

        # Rotate X-axis labels for better readability
        trace1.update_xaxes(tickangle=45)

        # Change the size of the figure
        trace1.update_layout(width=1200, height=600)

        # Change the theme (color scheme)
        trace1.update_layout(template="plotly_dark")






        custom_colors = ['#1000F2','#F70000']



        trace2 = px.pie(df, names='ISP', values='amount', title='Total Expenditure by ISP' , color_discrete_sequence=custom_colors, template="plotly_dark", width=800, height=500)
        # fig.add_trace(trace1, row=1, col=1)
        # fig.add_trace(trace2, row=1, col=2)

        # fig.update_layout(title='test', showlegend=True)
        trace2.update_layout(
        title={
            'text': "Total Expenditure by ISP",
            'x': 0.5,  # Title position (centered)
            'xanchor': 'center',  # Title anchor point
            'y': 0.95,  # Title Y position
            'yanchor': 'top',  # Title Y anchor point
            'font': {'size': 24}  # Adjust the font size as needed
        }
        )



    
        # Plot!
        st.plotly_chart(trace1, use_container_width=True)
        st.plotly_chart(trace2, use_container_width=True)