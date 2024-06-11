import math
import argparse 
from ultralytics import YOLO
import cv2
import numpy as np
import torch
import time
from model import TFLite

import graphics2d

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--src', help='Input Source, can be camera feed or video file', type=str, default="0")
    parser.add_argument('--model', help='Ultralytics model', type=str, default="models/face_det.pt")
    parser.add_argument('--pooled_img_width', help='Width of pooled img', type=int, default=96)
    parser.add_argument('--pooled_img_height', help='Height of pooled img', type=int, default=96)
    parser.add_argument('--base_sz', help='Height of image w/o HiRISE', type=str, default="140,140")
    parser.add_argument('--bbox_margin', help='Extra space around bbox', type=float, default=0.1)
    parser.add_argument('--gray', action='store_true')
    parser.add_argument('--timer', help='Time before demo ends', type=int, default=-1)
    parser.add_argument('--out', help='', type=str, default="demo")
    args = parser.parse_args()
    args.src = int(args.src) if args.src.isnumeric() else args.src
    person_model = YOLO(args.model)

    view = graphics2d.MainDisplay() # This is the window we are rendering (cv2 backend)
    cap = cv2.VideoCapture(args.src) # Source of video
    out = cv2.VideoWriter(f'{args.out}_gray.mp4' if not args.gray else f'{args.out}.mp4',
                          cv2.VideoWriter_fourcc(*'mp4v'), 30, (view.cv2().shape[1], view.cv2().shape[0])) # Output (video)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Loop to continuously read frames from the camera
    """""""""""""""
    Default  Values
    """""""""""""""
    nc = 3 if not args.gray else 1 # Number of color channels
    bw,bh = int(args.base_sz.split(",")[0]), int(args.base_sz.split(",")[1]) # Image size (w/o HiRISE)
    hx,hy,hw,hh = 0,0,0.1,0.1 # default values for bbox
    peak_img_sram_hirise = (args.pooled_img_width*args.pooled_img_height*nc) # HiRISE
    peak_img_sram_baseln = bw*bh*3
    bandwidth_hirise = 0
    bandwidth_baseln = 0
    avg_box_pixels_bl = 0
    avg_box_pixels_hr = 0
    num_frames = 0
    start_time = time.time()

    while True: # Main loop while video feed is open
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        frame = cv2.resize(frame, (640, 480))
        num_frames+=1
        frame_scaled = cv2.resize(frame, (args.pooled_img_width, args.pooled_img_height))

        if args.gray:
            frame_scaled = cv2.cvtColor(frame_scaled, cv2.COLOR_BGR2GRAY)
            frame_scaled = np.stack((frame_scaled,)*3, axis=-1)
        view.update_main(frame_scaled)
        main_canvas = view.get_main_canvas().astype(np.uint8).copy()

        head_results_hirise = person_model.track(frame_scaled,
                                                 verbose=False,
                                                 persist=True,
                                                 classes=[1],
                                                 tracker="botsort.yaml",
                                                 imgsz=args.pooled_img_width)
        
        frame_scaled = cv2.resize(frame, (bw, bh))
        x,y,w,h = 0,0,0,0
        bandwidth_hirise += (args.pooled_img_width*args.pooled_img_height*nc)
        bandwidth_baseln += bw*bh*3
        if len(head_results_hirise[0].boxes) > 0:
            for j, headbox in reversed(list(enumerate(head_results_hirise[0].boxes))):
                # Ultralytics uses X,Y,W,H bounding box coordinates (x,y are center of bbox)
                # https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format

                head_relative_xywh = np.concatenate(
                    [headbox.xywh.numpy()[0,:2] / np.array(headbox.orig_shape)[::-1],
                    headbox.xywh.numpy()[0,2:] / np.array(headbox.orig_shape)[::-1]]) # Convert bbox to coordinates relative to img size
                hx,hy,hw,hh = list(head_relative_xywh) # Turn them into a list
                peak_img_sram_hirise = max(peak_img_sram_hirise, hw*hh*3)
                
                graphics2d.draw_bbox_on_image(main_canvas, x+hx-w/2,y+hy-h/2,hw,hh,
                                              color=view.hirise_color if j==0 else view.baseline_color)
        
                head_image_hirise = graphics2d.crop_image_by_relative_coords(frame, x+hx-w/2,y+hy-h/2,hw,hh, center=True)
                head_image_baseline = graphics2d.crop_image_by_relative_coords(frame_scaled, x+hx-w/2,y+hy-h/2,hw,hh, center=True)
                head_image_hirise = cv2.resize(head_image_hirise, (args.pooled_img_width, args.pooled_img_height))
                bandwidth_hirise+=head_image_hirise.shape[0]*head_image_hirise.shape[0]*3
        avg_box_pixels_bl += head_image_baseline.shape[0]*head_image_baseline.shape[0]*3
        avg_box_pixels_hr += head_image_hirise.shape[0]*head_image_hirise.shape[0]*3

        view.update_hirise(head_image_hirise)
        view.update_baseline(head_image_baseline)
        view.update_main(main_canvas)
        disp = view.cv2()
        out.write(disp)
        cv2.imshow('Webcam', disp)

        # Check for 'q' key pressed to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time.time()-start_time > args.timer and not args.timer==-1:
            break

    # Release the camera and close OpenCV windows
    print("Peak Image SRAM")
    print(f"HiRISE: {peak_img_sram_hirise}")
    print(f"BaseLn: {peak_img_sram_baseln}")
    print()
    print("Avg Bandwidth")
    print(f"HiRISE: {bandwidth_hirise/num_frames: 0.1f}")
    print(f"BaseLn: {bandwidth_baseln/num_frames: 0.1f}")
    print()
    print("Avg Box Resolution")
    print(f"HiRISE: {avg_box_pixels_hr/num_frames: 0.1f}")
    print(f"BaseLn: {avg_box_pixels_bl/num_frames: 0.1f}")
    cv2.destroyAllWindows()
    out.release()
