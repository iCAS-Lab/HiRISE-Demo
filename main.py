import argparse 
from ultralytics import YOLO
import graphics2d
import cv2

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--src', help='Input Source', type=str, default="0")
    parser.add_argument('--model', help='Ultralytics model', type=str, default="models/face_det.pt")
    args = parser.parse_args()
    args.src = int(args.src) if args.src.isnumeric() else args.src
    model = YOLO(args.model)
    view = graphics2d.MainDisplay()
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Loop to continuously read frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        results = model.track(frame, persist=True, classes=[1], tracker="bytetrack.yaml", verbose=True, imgsz=320)
        annotated_frame = results[0].plot()
        # Display the captured frame
        view.update_main(annotated_frame)
        
        disp = view.cv2()
        cv2.imshow('Webcam', disp)

        # Check for 'q' key pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cv2.destroyAllWindows()
