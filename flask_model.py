from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
from flask_cors import CORS
import logging



#global variable for testing
var = 0

app = Flask(__name__)
CORS(app, supports_credentials=True)
logging.basicConfig(level=logging.INFO)



# Path to the folder containing images
#IMAGE_FOLDER = 'Desktop/VisualPaste/FirstApp/static'
IMAGE_FOLDER = 'static'

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            img_path = os.path.join(folder, filename)
            images.append(filename)  # Store just the filename for display
    return images

def process_image_to_grey(image_path):
     # Read the image using OpenCV
    img = cv2.imread(image_path)
    
    # Convert the image to HSV
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert to PIL Image for easy manipulation
    hsv_image_pil = Image.fromarray(hsv_image)
    
    return hsv_image_pil

def load_images_from_folder_grey(folder):
    images1 = []

    # Loop through all files in the directory
    for filename in os.listdir(IMAGE_FOLDER):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Add more formats as needed
            image_path = os.path.join(IMAGE_FOLDER, filename)
            hsv_image = process_image_to_grey(image_path)
            # Save the image to a BytesIO object
            img_io = io.BytesIO()
            hsv_image.save(img_io, 'PNG')
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            # Append the image file-like object to the list
            images1.append((filename, img_base64))
    return images1

def count_seeds_and_peels(image_path):
    img = cv2.imread(image_path)
    
    blur = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    thresh_for_black_dots = cv2.threshold(gray,100,255, cv2.THRESH_BINARY_INV)[1]
    thresh_for_white_dots = cv2.threshold(gray,200,255, cv2.THRESH_BINARY)[1]

    cnts_for_black_dots = cv2.findContours(thresh_for_black_dots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_for_white_dots = cv2.findContours(thresh_for_white_dots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts_for_black_dots = cnts_for_black_dots[0] if len(cnts_for_black_dots) == 2 else cnts_for_black_dots[1]
    cnts_for_white_dots = cnts_for_white_dots[0] if len(cnts_for_white_dots) == 2 else cnts_for_white_dots[1]

    min_area = 1
    black_dots = []
    white_dots = []

    for c in cnts_for_white_dots:
        area = cv2.contourArea(c)
        if area > min_area:
            cv2.drawContours(img, [c], -1, (36, 255, 12), 2)
            black_dots.append(c)
            white_dots.append(c)
        
    for c in cnts_for_black_dots:
        area = cv2.contourArea(c)
        if area > min_area:
            cv2.drawContours(img, [c], -1, (36, 255, 12), 2)
            black_dots.append(c) 
    return len(black_dots)

def count_anomalies_in_folder(folder):
    image_anomalies = {}
    images = load_images_from_folder(folder)
    
    for filename in images:
        image_path = os.path.join(folder, filename)  # Create full path
        #count = count_anomalies(image_path)  # Pass the full path
        count = count_seeds_and_peels(image_path)
        image_anomalies[filename] = count
        
    #print(image_anomalies)

    return image_anomalies

@app.route('/images')
def index():
    images = load_images_from_folder(IMAGE_FOLDER)
    return render_template('index.html', images=images)

@app.route('/count_anomalies')
def index1():
    #get count of anomalies per image in folder
    count = count_anomalies_in_folder(IMAGE_FOLDER)
    #convert into json file
    count1 = json.dumps(count)
    #var = count1
    #print(var)
    
    pics = load_images_from_folder_grey(IMAGE_FOLDER)
    
    return render_template('index2.html', json_data=count1, images=pics)


#print(var)

#display json output from the anomaly detection count
@app.route('/output')
def index2():
    app.logger.info(var)
    return render_template('index3.html', json_d = var)

#display json output from the anomaly detection count
# @app.route('/output1', methods=['GET'])
# def index3():
#     return jsonify(var)

var = json.dumps(count_anomalies_in_folder(IMAGE_FOLDER))
#python script to save json output to a file called data.json
f_name = 'data.json'
with open(f_name, 'w') as json_file:
    json.dump(var, json_file, indent=4)

if __name__ == "__main__":
    app.run(debug=True)