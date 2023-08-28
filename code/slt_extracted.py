#!/usr/bin/env python
# coding: utf-8

# In[20]:


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


# In[21]:


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'   


# In[40]:


df = pd.read_csv('../files/isp_data.csv')


# In[41]:


# delete all records where ISP = "SLT"
df = df[df.ISP != 'SLT']


# In[42]:


def convert_date(date_str):
    try:
        # Attempt to parse the date in "month/day/year" format
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        # Convert it to "year-month-day" format
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        # If the date is already in "year-month-day" format or is not a valid date, return it as is
        return date_str


# In[43]:


# Replace 'your_folder_path' with the path to your folder containing images
folder_path = '../Data/Internet_bills_slt'

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Filter the list to keep only image files (you can add more extensions if needed)
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
image_files = [f for f in file_list if any(f.lower().endswith(ext) for ext in image_extensions)]




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
        image = enhancer.enhance(1.2)  # Increase brightness by 20%

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # Increase contrast by 20%

        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)  # Increase saturation by 20%

        # show the image
        # image.show()

        # image = image.filter(ImageFilter.CONTOUR)


        # image.show()


        width, height = image.size


        date_box_coordinates = (105, 284, 713, 661)
        amount_box_coordinates = (89, 958, 1587, 1500)

    

        date_cropped_image = image.crop(date_box_coordinates)
        # date_cropped_image = date_cropped_image.filter(ImageFilter.EDGE_ENHANCE)


        amount_cropped_image = image.crop(amount_box_coordinates)
        # amount_cropped_image = amount_cropped_image.filter(ImageFilter.EDGE_ENHANCE)


        # date_cropped_image.show()
        # amount_cropped_image.show()
    
        text = pytesseract.image_to_string(image)
        text_date = pytesseract.image_to_string(date_cropped_image)
        text_amount = pytesseract.image_to_string(amount_cropped_image)


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





        # replace | and [ with space
        # text_logo = text_logo.replace('|', '')
        # text_logo = text_logo.replace('[', '')

        text_date = text_date.replace('|', '')
        text_date = text_date.replace('[', '')

        text_amount = text_amount.replace('|', '')
        text_amount = text_amount.replace('[', '')

        # print(text_date)
        # print(text_amount)

        # print("========================================================================================================")


        # Define a regular expression pattern to match the billing date
        billing_date_pattern = r'Billing Date\s+(\d{2}/\d{2}/\d{4})'

        # Search for the billing date using the pattern
        billing_date_match = re.search(billing_date_pattern, text_date)

        # Extract and print the billing date if found
        if billing_date_match:
            billing_date = billing_date_match.group(1)
            # print(f"Billing Date: {billing_date}")
        else:
            print("Date not found: " , text_date)



        # Define a regular expression pattern to match the total charges for the period
        total_charges_pattern = r'Total Charges for the Period\s+([\d,.]+)'

        # Search for the total charges using the pattern
        total_charges_match = re.search(total_charges_pattern, text_amount)

        # Extract and print the total charges if found
        if total_charges_match:
            total_charges = total_charges_match.group(1)
            # Remove commas and convert to float
            total_charges = float(total_charges.replace(',', ''))
            # print(f"Total Charges for the Period: {total_charges:.2f}")
        else:
            print("Total not found: " , text_amount)

        # print("all:" , text_all)


        billing_date = convert_date(billing_date)




        df = df.append({'image_path': image_path,'ISP':isp, 'date': billing_date, 'amount': total_charges}, ignore_index=True)


        print("========================================================================================================")
    
    except Exception as e:
        print(f"Error opening {image_file}: {str(e)}")




# In[47]:


# get year and month from date
df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month


# In[48]:


df


# In[46]:


# save to csv
df.to_csv('../files/isp_data.csv', index=False)


# In[ ]:




