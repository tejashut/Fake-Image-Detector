from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os

def perform_error_level_analysis(image_path, quality):
    original_image = Image.open(image_path).convert("RGB")
    resaved_file_name = "resaved_image.jpg"
    original_image.save(resaved_file_name, "JPEG", quality=quality)
    resaved_image = Image.open(resaved_file_name)
    ela_image = ImageChops.difference(original_image, resaved_image)
    extrema = ela_image.getextrema()
    max_difference = max([pix[1] for pix in extrema])
    if max_difference == 0:
        max_difference = 1
    scale = 255.0 / max_difference
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    os.remove(resaved_file_name)
    edited_percentage = detect_edits(ela_image)
    result = {
        'edited_percentage': edited_percentage,
        'edited': edited_percentage > 5
    }
    return result

def detect_edits(ela_image, threshold=10):
    pixels = ela_image.getdata()
    edited_pixels = [pixel for pixel in pixels if pixel[0] > threshold]
    edited_percentage = (len(edited_pixels) / len(pixels)) * 100
    return edited_percentage
