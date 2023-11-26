import os
import shutil
import cv2
import pytesseract
import re


# Set the path to the folder containing the pictures
path = r'13.9.22_pythonislands'

# Set the path to the output folder
output_path = r'13.9.22_pythonislands_renamed'

# Set the changeable text
picture_name = ''

# Loop through all the files in the folder
for filename in os.listdir(path):
    # Check if the file is an image
    if filename.endswith('.jpeg') or filename.endswith('.JPG'):
        # Load the image
        img = cv2.imread(os.path.join(path, filename))
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to the image
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Apply dilation to the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilated = cv2.dilate(thresh, kernel, iterations=4)
        
        # Find contours in the image
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Loop over the contours
        for contour in contours:
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Crop the contour from the image
            roi = img[y:y+h, x:x+w]
            
            # Apply OCR to the cropped contour
            text = pytesseract.image_to_string(roi, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            match = re.search(r"\d{6}", text)
            if match:
                # Get the matched string
                text = match.group(0)
                print(text)
                # Filter out the 6 digit number from the recognized text
                number = ''.join(filter(str.isdigit, text))
                
                # Set the new filename
                new_filename = f'{picture_name}{number}.jpeg'
                
                # Check if the new filename already exists
                i = 1
                while os.path.exists(os.path.join(output_path, new_filename)):
                    new_filename = f'{picture_name}{number}_{i}.jpeg'
                    i += 1
                
                # Copy the original file to the output folder with the new name
                shutil.copy(os.path.join(path, filename), os.path.join(output_path, new_filename))
                print("Read from: " + filename)
                break
