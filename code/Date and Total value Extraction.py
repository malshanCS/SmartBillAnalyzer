#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import numpy as np
import pandas as pd
from PIL import Image
import pytesseract
import cv2
import os
import numpy as np
import re 
# import moment
from datetime import datetime
import csv
from pytesseract import Output


# In[2]:


import sys
get_ipython().system('{sys.executable} -m pip install pytesseract')


# In[3]:


# method to get the text from image 
def extract_datetext(image):
    
    #save the gray image
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, image)

    # load the image as a PIL/Pillow image, apply OCR
    text = pytesseract.image_to_string(Image.open(filename))
    text = text.replace('\n', ' ').replace('\r', '')
    
    # date extraction pattern
    pat1 = r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n\s:](0?[1-9]|1[0-2])[^\w\d\r\n\s:](\d{4}|\d{2})\b)'
    pat2 = r'(\b(0?[1-9]|1[0-2])[^\w\d\r\n\s:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n\s:](\d{4}|\d{2})\b)'
    pat3 = r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n\s:](0?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\w\d\r\n\s:](\d{4}|\d{2})\b)'
    pat4 = r'(\b(0?Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)'
    pat5 = r'(\b(\d{4})[^\w\d\r\n\s:](0?[1-9]|1[0-2])[^\w\d\r\n\s:](0?[1-9]|[12]\d|30|31)\b)'

    #combine all the five pattern
    combined_pat = r'|'.join((pat1, pat2, pat3, pat4, pat5))
    pattern = re.compile(combined_pat, re.IGNORECASE)
    #get the date
    extract_date = re.search(pattern,text)
    if extract_date is not None:
        date = extract_date.group()
    else:
        date = "empty"   
    return date



# In[4]:


def date_extractor(file_path):
    image_file = set_image_dpi(file_path)
    image = remove_noise_and_smooth(image_file)
    date_text = extract_datetext(image)
    if date_text == "empty":
        image = using_hsv_extract(image_file)
        date_text = extract_datetext(image)
    
    if date_text == "empty":
        date_text = "null"
    else:
        date_text = moment.date(date_text).strftime('%Y-%m-%d')

    #remove the temporary file 
    os.remove(image_file)    

    return date_text


# In[5]:


import cv2
import pytesseract
import re
import numpy as np

def extract_total_value(image_path):
    try:
        img = cv2.imread(image_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6'
        ocr_output_details = pytesseract.image_to_data(thresh_img, output_type=pytesseract.Output.DICT, config=custom_config, lang='eng')

        total_variations = ["Total", "Total due", "Due","TOTL"]
        total_index = None

        for i in range(len(ocr_output_details['text']) - 1, -1, -1):
            word = ocr_output_details['text'][i]
            if any(variation in word for variation in total_variations):
                total_index = i
                break

        if total_index is not None:
            total_x = ocr_output_details['left'][total_index]
            total_y = ocr_output_details['top'][total_index]
            total_width = ocr_output_details['width'][total_index]
            total_height = ocr_output_details['height'][total_index]
            y_range = range(total_y - 10, total_y + total_height + 10)
            selected_boxes = []

            for i, word in enumerate(ocr_output_details['text']):
                if any(char.isdigit() for char in word) and ocr_output_details['top'][i] in y_range:
                    selected_boxes.append(i)

            largest_box_index = None
            largest_box_area = 0

            for box_index in selected_boxes:
                box_area = ocr_output_details['width'][box_index] * ocr_output_details['height'][box_index]
                if box_area > largest_box_area:
                    largest_box_area = box_area
                    largest_box_index = box_index

            if largest_box_index is not None:
                x = ocr_output_details['left'][largest_box_index]
                y = ocr_output_details['top'][largest_box_index]
                w = ocr_output_details['width'][largest_box_index]
                h = ocr_output_details['height'][largest_box_index]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                box_text = ocr_output_details['text'][largest_box_index]
                numerical_values = re.findall(r'\d+\.\d+|\d+', box_text)

                if numerical_values:
                    largest_value = max(float(val) for val in numerical_values)
                    return largest_value
                else:
                    return np.nan
            else:
                return np.nan
        else:
            return np.nan

    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return np.nan


# In[6]:


current_directory = os.getcwd()
print("Current Working Directory:", current_directory)


# In[8]:


# Replace 'your_folder_path' with the path to your folder containing images
folder_path = '../Data/Background removed'

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Filter the list to keep only image files (you can add more extensions if needed)
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
image_files = [f for f in file_list if any(f.lower().endswith(ext) for ext in image_extensions)]



# In[9]:


# Create an empty DataFrame
columns = ['image_path', 'date', 'amount']
df= pd.DataFrame(columns=columns)
csv_filename = "../files/Receipt_data.csv"
# Check if the CSV file exists, if not, create it
if not os.path.exists(csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(columns)




# In[10]:


for image_file in image_files:
    # Construct the full path to the image file
    image_path = os.path.join(folder_path, image_file)
    img = cv2.imread(image_path)
    try:
        date = extract_datetext(img)
        total = extract_total_value(image_path)
        new_data = pd.DataFrame({'image_path': [image_path], 'date': [date], 'amount': [total]})
        df = pd.concat([df, new_data], ignore_index=True)
    except Exception as e:
        print(e)
        
df.to_csv(csv_filename, index=False)


# In[ ]:





# In[ ]:




