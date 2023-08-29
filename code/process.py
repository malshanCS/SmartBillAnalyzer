#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import nltk
import pandas as pd
import re
from PIL import Image, ImageFilter
from PIL import Image, ImageEnhance
import os
from datetime import datetime


# In[ ]:


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'   


# In[ ]:


csv_file = '../files/isp_data_2.csv'
if not os.path.isfile(csv_file):
    # If the file doesn't exist, create it with a header
    df = pd.DataFrame(columns=['image_path', 'ISP', 'date', 'amount'])
    df.to_csv(csv_file, index=False)
else:
    # If the file exists, append the data to the DataFrame
    df = pd.read_csv(csv_file)


# In[ ]:


def convert_date(date_str):
    try:
        # Attempt to parse the date in "month/day/year" format
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        # Convert it to "year-month-day" format
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        # If the date is already in "year-month-day" format or is not a valid date, return it as is
        return date_str


# In[ ]:


folder_path = '../Data/batch_process'

# Get a list of all files in the folder
file_list = os.listdir(folder_path)


# Filter the list to keep only image files (you can add more extensions if needed)
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
image_files = [f for f in file_list if any(f.lower().endswith(ext) for ext in image_extensions)]


# In[ ]:


def check_isp(text):
        # Initialize the isp variable to None
        isp = "Unknown"

        # Check for "Dialog" or "myDialog"
        dialog_pattern = r'\b(?:my)?dialog\b'
        if re.search(dialog_pattern, text, re.IGNORECASE):
            isp = "Dialog"

        # Check for "SLT" or "Sri Lanka Telecom"
        slt_pattern = r'\bslt\b|\bsri\s+lanka\s+telecom\b'
        if re.search(slt_pattern, text, re.IGNORECASE):
            isp = "SLT"

        # Check for "Hutch"
        hutch_pattern = r'\bhutch\b'
        if re.search(hutch_pattern, text, re.IGNORECASE):
            isp = "Hutch"

        return isp


# In[ ]:


def get_date_amount(date_box_coordinates, amount_box_coordinates, image):
            date_cropped_image = image.crop(date_box_coordinates)
            amount_cropped_image = image.crop(amount_box_coordinates)


            text_date = pytesseract.image_to_string(date_cropped_image)
            text_amount = pytesseract.image_to_string(amount_cropped_image)


            text_date = text_date.replace('|', '')
            text_date = text_date.replace('[', '')

            text_amount = text_amount.replace('|', '')
            text_amount = text_amount.replace('[', '')

            return text_date, text_amount

            
    


# In[ ]:


# Loop through the image files and open each one
for image_file in image_files:
    # Construct the full path to the image file
    image_path = os.path.join(folder_path, image_file)


    if image_path in df['image_path'].tolist():
        print(f"Skipping image {image_file} as it's already in the DataFrame.")
        continue

        # Open the image using PIL
    try:
        image = Image.open(image_path)
        # print(image_path)

        if image.mode == "P":
        # Convert the image to RGB mode
            image = image.convert("RGB")

        # image.show()


        image = image.filter(ImageFilter.EDGE_ENHANCE)

        # Enhance the brightness, contrast, and saturation
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.5)  # Increase brightness by 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.8)  # Increase contrast by 20%

        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.8)  # Increase saturation by 20%


        width, height = image.size

        text = pytesseract.image_to_string(image)
    
        isp = check_isp(text)


        if isp == 'SLT':
            date_box_coordinates = (105, 284, 713, 661)
            amount_box_coordinates = (693, 755, 964, 939)

            text_date, text_amount = get_date_amount(date_box_coordinates, amount_box_coordinates, image)


            # Define a regular expression pattern to match the billing date
            billing_date_pattern = r'Billing Date\s+(\d{2}/\d{2}/\d{4})'

            # Search for the billing date using the pattern
            billing_date_match = re.search(billing_date_pattern, text_date)

            # Extract and print the billing date if found
            if billing_date_match:
                billing_date = billing_date_match.group(1)
                # print(f"Billing Date: {billing_date}")
            else:
                print("Date not found: " , image_path)
                billing_date = np.NaN


            # Define a regular expression pattern to match the total charges for the period
            total_charges_pattern = r'Charges for the period\s+([\d,.]+)'

            # Search for the total charges using the pattern
            total_charges_match = re.search(total_charges_pattern, text_amount)

            # Extract and print the total charges if found
            if total_charges_match:
                total_charges = total_charges_match.group(1)
                # Remove commas and convert to float
                total_charges = float(total_charges.replace(',', ''))
                # print(f"Total Charges for the Period: {total_charges:.2f}")
            else:
                print("Total not found: " , image_path)
                total_charges = np.NaN


            billing_date = convert_date(billing_date)


        elif isp == 'Dialog':
            
            date_box_coordinates = (27, 284, 231, 517)
            amount_box_coordinates = (296, 300, 772, 555) 

            text_date, text_amount = get_date_amount(date_box_coordinates, amount_box_coordinates, image)



            # Define a regular expression pattern to match the billing date
            billing_date_pattern = r'Date\s+(\d{4}-\d{2}-\d{2})'

            # Search for the billing date using the pattern
            billing_date_match = re.search(billing_date_pattern, text_date)

            # Extract and print the billing date if found
            if billing_date_match:
                billing_date = billing_date_match.group(1)
                # print(f"Billing Date: {billing_date}")
            else:
                print("Date not found: " , image_path)
                billing_date = np.NaN



            # Define a regular expression pattern to match the total charges for the period
            total_charges_pattern = r'Total\s+([\d,.]+)'

            # Search for the total charges using the pattern
            total_charges_match = re.search(total_charges_pattern, text_amount)

            # Extract and print the total charges if found
            if total_charges_match:
                total_charges = total_charges_match.group(1)
                # Remove commas and convert to float
                total_charges = float(total_charges.replace(',', ''))
                # print(f"Total Charges for the Period: {total_charges:.2f}")
            else:
                print("Total not found: " , image_path)
                total_charges = np.NaN




        df = df.append({'image_path': image_path,'ISP':isp, 'date': billing_date, 'amount': total_charges}, ignore_index=True)

        print("========================================================================================================")


    except Exception as e:
        print(f"Error opening {image_file}: {str(e)}")
        

# save the dataframe as a csv file
df.to_csv('../files/isp_data_2.csv', index=False)




# In[ ]:


# df = pd.read_csv('../files/isp_data_2.csv')
# df


# In[ ]:




