"""
Object Detection Module
-----------------------

This script performs basic object detection on a sample drone video 
(`drone-in-sky-for-ml_slowed.mp4`) using OpenCV.  
It applies adaptive thresholding, contour approximation, and bounding box 
prediction through a purely mathematical model.

Note:
Originally, we considered using pre-trained deep learning models such as 
YOLO for robust object detection.  
However, as per judges' feedback and SIH hackathon guidelines, the 
idea of using heavy pre-trained models was not pursued.  

Instead, this implementation demonstrates an algorithmic approach using 
OpenCV, which keeps computation lightweight while fulfilling the project 
requirements.
"""

import cv2

def detect_boxes_improved_close_objects():
    cap = cv2.VideoCapture('drone-in-sky-for-ml_slowed.mp4')

    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    cv2.namedWindow('Object Detection', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Object Detection', 200, 200)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # Adaptive threshold - better for uneven lighting
        thresh = cv2.adaptiveThreshold(blurred, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        morph = cv2.dilate(morph, kernel, iterations=2)

        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            if area < 800:
                continue

            epsilon = 0.05 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if 4 <= len(approx) <= 8:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)

                if 0.25 <= aspect_ratio <= 4.0:
                    if cv2.isContourConvex(approx):
                        color = (0, 255, 0)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        cv2.putText(frame, f'{w}x{h}', (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        cv2.imshow('Object Detection', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_boxes_improved_close_objects()
