import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
import streamlit as st
from streamlit_option_menu import option_menu

# read the dataframe from ../data/isp_data_2.csv
df = pd.read_csv("../files/isp_data_2.csv")



def plot(df):
    x_axis_val = st.selectbox("Select the x-axis value", options=df.columns)
    y_axis_val = st.selectbox("Select the y-axis value", options=df.columns)

    plot = px.scatter(df, x=x_axis_val, y=y_axis_val, color="ISP")
    st.plotly_chart(plot)


plot(df)