import argparse 
from ultralytics import YOLO
import graphics2d
import cv2
import numpy as np
import math
from model import TFLite

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--src', help='Input Source', type=str, default="0")
    parser.add_argument('--model', help='Ultralytics model', type=str, default="models/face_det.pt")
    parser.add_argument('--width', help='Width of image', type=int, default=64)
    parser.add_argument('--height', help='Height of image', type=int, default=64)
    parser.add_argument('--bbox_margin', help='Extra space around bbox', type=float, default=0.1)
    args = parser.parse_args()
    args.src = int(args.src) if args.src.isnumeric() else args.src
    model = YOLO(args.model)
    facial_expression_model = TFLite("models/facial_expression/mbnet-R112_float16.tflite",
                                     labels=["Anger", "Disgust",
                                             "Fear", "Happiness",
                                             "Neutral", "Sadness", "Surprise"])
    view = graphics2d.MainDisplay()
    cap = cv2.VideoCapture(args.src)

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
        
        frame_scaled = cv2.resize(frame, (args.width, args.height))
        view.update_main(frame_scaled)
        main_canvas = view.get_main_canvas().astype(np.uint8).copy()

        results = model.track(frame, persist=True, classes=[1], tracker="bytetrack.yaml", verbose=False, imgsz=args.width)
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                relative_xywh = np.concatenate([box.xywh.numpy()[0,:2] / np.array(box.orig_shape)[::-1],
                                box.xywh.numpy()[0,2:] / np.array(box.orig_shape)[::-1]])
                x,y,w,h = list(relative_xywh)

                box_image_baseline = graphics2d.crop_image_by_relative_coords(frame_scaled, x,y,w,h, center=True)
                box_image_hirise = graphics2d.crop_image_by_relative_coords(frame, x,y,w,h, center=True)
                graphics2d.draw_bbox_on_image(main_canvas, x, y, w, h)

            # Display the captured frame
            view.update_main(main_canvas)
            view.update_baseline(box_image_baseline)
            view.update_hirise(box_image_hirise)

        model_pred_baseline = facial_expression_model(box_image_baseline)
        model_pred_hirise = facial_expression_model(box_image_hirise)
        
        print("HiRISE:", model_pred_hirise)
        print("Baseline:", model_pred_baseline)
        disp = view.cv2()
        cv2.imshow('Webcam', disp)

        # Check for 'q' key pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cv2.destroyAllWindows()
