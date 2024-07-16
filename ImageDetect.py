import cv2
import numpy as np
from ultralytics import YOLO



# Load the YOLO model
model = YOLO('yolov8n.pt')

# Draw bounding boxes
def draw_boxes(frame, results, confidence_threshold=0.3):
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = box.cls[0]

            if conf > confidence_threshold:
                label = f"{model.names[int(cls)]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Open video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model.track(frame, persist=True)

    # Draw bounding boxes on the frame
    draw_boxes(frame, results)
   # Plot results 
    frame_ = results[0].plot()

    # Show the frame with detections
    cv2.imshow('frame', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
