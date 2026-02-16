# Real-Time-Stock-Management-System-for-Retail-Store
Developed AI-based stock monitoring system using YOLOv8 and Roboflow. 
It tracks the empty and filled spaces in the racks by capturing images using real time observation through camera setup. Trained model on 10,000+ shelf images for filled vs empty detection.
Achieved 92% precision in stock classification and real-time processing (30+ FPS).
Integrated alert system for low-stock notifications.
Technologies: Python, YOLOv8, OpenCV, Roboflow, Google Colab.
Real-Time-Stock-Management-System-for-Retail-Store is a revolutionizing retail stock management by automating inventory tracking, reducing manual labor, and enhancing operational efficiency. This technology enables real-time monitoring of stock levels, ensuring timely restocking and optimized inventory management. It improves customer experience by maintaining product availability and streamlining checkout processes. Additionally, image recognition provides valuable data insights for customer behavior analysis and demand forecasting, while also enhancing security through theft detection. As a result, retailers can achieve greater accuracy, efficiency, and customer satisfaction in their operations.
The integration of image recognition in retail facilitates timely restocking, prevents stockouts, and maintains optimal inventory levels, leading to improved customer satisfaction and reduced labor costs. Additionally, this technology supports the optimization of shelf space by ensuring products are displayed according to planograms, thus enhancing their visibility and availability. Retailers can also utilize predictive analytics derived from image recognition data to forecast demand more accurately, enabling smarter procurement strategies that mitigate overstock and stockout situations.
#Algorithm
For single image: 
Algorithm for Object Detection Using Roboflow in Google Colab 
1. Setup Environment: 
 Install the roboflow package. 
 Import necessary libraries: cv2, numpy, Roboflow, and cv2_imshow from Colab 
patches. 
2. Initialize Roboflow Model: 
 Create a Roboflow instance using the API key. 
26 
 Access the desired project and model version. 
3. Load Image: 
 Load an image from the specified path (/content/test_image.jpg). 
4. Make Predictions: 
 Use the model to predict objects in the image. 
 Retrieve predictions in JSON format. 
5. Process Predictions: 
 Initialize counters for different object classes (e.g., "filled" and "empty"). 
 Iterate over each prediction: 
 Extract class name and bounding box coordinates (x, y, width, height). 
 Determine color for bounding box based on class (e.g., green for "filled", red for 
"empty"). 
 Calculate bottom-right corner coordinates of the bounding box. 
 Draw rectangle on the image using cv2.rectangle. 
 Append bounding box data to a list for further use. 
6. Display Results: 
 Show the image with bounding boxes using cv2_imshow. 
 Print counts of each class. 
 Print details of each detected box. 
Key Points 
 Bounding Boxes: Visualize detected objects with rectangles. 
 Class Counting: Keep track of how many objects belong to each class. 
 Output: Display processed image and print relevant information. 
This algorithm is designed to detect and classify objects in images using a pre-trained model hosted on Roboflow, specifically within
a Google Colab environment. Adjust API keys, project names, and version numbers as needed for your specific use case.

For multiple images 
1. Setup and Initialization: 
 Install necessary packages: roboflow, opencv-python-headless, etc.
 Import required libraries: cv2 and Roboflow. 
 Initialize the RoboFlow model with API key, project name, and version. 
2. Video Capture: 
 Open the default camera using cv2.VideoCapture(). 
 Check if the camera is accessible; exit if not. 
3. Main Loop: 
 Continuously capture frames from the camera. 
 For each frame: 
 Use the RoboFlow model to predict objects. 
 Initialize counters for different classes (e.g., "Filled", "Empty"). 
4. Object Detection and Annotation: 
 Iterate through predictions: 
 Extract bounding box coordinates and class names. 
 Count occurrences of each class. 
 Assign colors based on class (e.g., green for "Filled", red for "Empty"). 
 Draw bounding boxes and labels on the frame. 
5. Display: 
 Show the processed frame in a window titled "Camera Feed". 
 Print counts of detected objects. 
6. Exit Condition: 
 Break the loop if 'q' is pressed. 
7. Cleanup: 
 Release the camera and close all OpenCV windows. 
This algorithm processes video frames in real-time to detect and annotate objects using a 
machine learning model, displaying results on the screen.
