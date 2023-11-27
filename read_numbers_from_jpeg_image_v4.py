import os
import shutil
import cv2
import pytesseract
import re

# Set the path to the folder containing the pictures
path = r'./28.9.22_wakhangarapoint'

# Set the path to the output folder
output_path = r'./28.9.22_wakhangarapoint_out'

# Set the changeable text
prefix = ''

file_count = 0
# Loop through all the files in the folder
for filename in os.listdir(path):
    file_count += 1
    # Check if the file is an image
    if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.JPG'):
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
        digits_found = False
        for contour in contours:
            match = False
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Crop the contour from the image
            roi = img[y:y+h, x:x+w]
            
            # Apply OCR to the cropped contour
            text = pytesseract.image_to_string(roi, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
            
            # Filter out the 6 digit number from the recognized text
            match = re.search(r"\d{6}", text)

            # Set the new filename
            if match:
                number = match.group(0)
                #number = ''.join(filter(str.isdigit, text))
                new_filename = f'{prefix}{number}.jpeg'
                print(number)
                digits_found = True
                
            

        if digits_found:
            # Check if the new filename already exists
            i = 1
            while os.path.exists(os.path.join(output_path, new_filename)):
                new_filename = f'{prefix}{number}_{i}.jpeg'
                i += 1

            # Copy the original file to the output folder with the new name
            n_filename = new_filename.replace('\n', '')
            #print("filename:"+new_filename)
            shutil.copy(os.path.join(path, filename), os.path.join(output_path, n_filename))
            #print("Files written")

        else:
            new_filename = filename
            # Check if the new filename already exists
            i = 1
            while os.path.exists(os.path.join(output_path, new_filename)):
                new_filename = f'{filename}_{i}.jpeg'
                i += 1
            shutil.copy(os.path.join(path, filename), os.path.join(output_path, new_filename))
            #print("NoDigits-File written")

print("Number of Files: "+ str(file_count))
