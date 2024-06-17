import cv2
import numpy as np
import matplotlib.pyplot as plt

def perform_gradient_descent(image_path):
    image = cv2.imread(image_path)
    result, percentage_changed = detect_background_changes(image)
    if result is not None:
        temp_file = 'masked_image.jpg'
        cv2.imwrite(temp_file, result)

        # Create a pie chart of background change detection percentage
        labels = ['Background', 'Changed']
        sizes = [100 - percentage_changed, percentage_changed]
        colors = ['#ff9999','#66b3ff']
        explode = (0, 0.1)  # explode the 2nd slice (i.e. 'Changed')
        
        plt.ioff()  # Turn off interactive mode
        plt.figure(figsize=(6,6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('background_change_pie_chart.jpg')  # Save the pie chart as an image
        plt.close()  # Close the Matplotlib figure
        
        return {'masked_image_path': temp_file, 'pie_chart_path': 'background_change_pie_chart.jpg'}
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
    if percentage_changed > 20:
        largest_contour = max(contours, key=cv2.contourArea)
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        return masked_image, percentage_changed
    else:
        return None, percentage_changed
