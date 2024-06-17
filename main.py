from flask import Flask, render_template, request, redirect, url_for,jsonify
from error_level_analysis import perform_error_level_analysis 
from gradient_descent import perform_gradient_descent 
from metadata_analysis import perform_metadata_analysis
import os
import matplotlib
matplotlib.use('Agg')
from PIL import Image
from werkzeug.utils import secure_filename
import cv2
from PIL import ImageChops,ImageEnhance
import numpy as np
import json

app = Flask(__name__)

# Ensure uploads directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload_image():
    # Check if the POST request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    # If user does not select file, browser also submits an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
            # Check if the uploaded file is a valid image
            img = Image.open(file.stream)
            img.verify()  # Verify the image file
            file.seek(0)  # Reset file pointer after verification
            
            # Save the uploaded file
            image_path = os.path.join('uploads', secure_filename(file.filename))
            file.save(image_path)

            # Perform image analysis and get the result
            result = image_analysis(image_path)
            
            # Redirect to the result route with the result as a query parameter
            return jsonify(result)#redirect(url_for('show_result', result=json.dumps(result)))
            
        except Exception as e:
            return jsonify({'error': str(e)})

    return jsonify({'error': 'Unknown error'})

def image_analysis(image_path):
    try:
        quality = 90

        # Perform Error Level Analysis
        ela_result = perform_error_level_analysis(image_path, quality)

        # Perform Gradient Descent
        gradient_result = perform_gradient_descent(image_path)

        # Perform Metadata Analysis
        metadata_result = perform_metadata_analysis(image_path)
        os.remove(image_path)
        # Combine results
        combined_result = {
            'error_level_analysis': ela_result,
            'gradient_descent': gradient_result,
            'metadata_analysis': metadata_result
        }

        return combined_result
    
    except FileNotFoundError:
        return {'error': 'Image file not found.'}
    
    except IOError as e:
        if 'not readable' in str(e):
            return {'error': 'Image file is not readable.'}
        elif 'not truncated' in str(e):
            return {'error': 'Image file is truncated.'}
        else:
            return {'error': str(e)}
    
    except Exception as e:
        return {'error': str(e)}



def perform_error_level_analysis(image_path, quality):
    original_image = Image.open(image_path).convert("RGB")
    resaved_file_name = "resaved_image.jpg"
    
    try:
        with original_image.copy() as image_copy:
            image_copy.save(resaved_file_name, "JPEG", quality=quality)
            
        resaved_image = Image.open(resaved_file_name)
        ela_image = ImageChops.difference(original_image, resaved_image)
        extrema = ela_image.getextrema()
        max_difference = max([pix[1] for pix in extrema])
        
        if max_difference == 0:
            max_difference = 1
        
        scale = 255.0 / max_difference
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        edited_percentage = detect_edits(ela_image)
        result = {
            'edited_percentage': edited_percentage,
            'edited': edited_percentage > 5
        }
        return result
    
    finally:
        # Make sure to close the resaved image file
        if os.path.exists(resaved_file_name):
            os.remove(resaved_file_name)


def detect_edits(ela_image, threshold=10):
    pixels = ela_image.getdata()
    edited_pixels = [pixel for pixel in pixels if pixel[0] > threshold]
    edited_percentage = (len(edited_pixels) / len(pixels)) * 100
    return edited_percentage

def perform_gradient_descent(image_path):
    image = cv2.imread(image_path)
    result = detect_background_changes(image)
    if result is not None:
        temp_file = 'masked_image.jpg'
        cv2.imwrite(temp_file, result)
        return {'masked_image_path': temp_file}
    else:
        return {'message': 'No background changes detected.'}

def detect_background_changes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    edges_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(edges_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total_area = image.shape[0] * image.shape[1]
    contour_areas = [cv2.contourArea(contour) for contour in contours]
    total_contour_area = sum(contour_areas)
    percentage_changed = (total_contour_area / total_area) * 100
    if percentage_changed > 40:
        largest_contour = max(contours, key=cv2.contourArea)
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        return masked_image
    else:
        return None

# @app.route('/result')
# def show_result():
#     # Retrieve the result from the query parameter
#     result_json = request.args.get('result')
#     result = json.loads(result_json) if result_json else {}

#     # Check if the result contains an error message
#     if 'error' in result:
#         return render_template('error.html', error=result['error'])

#     # Pass the result to the template
#     return render_template('result.html', result_json=result)

if __name__ == '__main__':
    app.run(debug=True)
