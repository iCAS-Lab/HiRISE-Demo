import time
import cv2
import numpy as np
from ultralytics import YOLO


class HiRISE():
    def __init__(self):
        self.pooled_img_width = 96
        self.pooled_img_height = 96
        self.model = './src/models/face_det.pt'
        self.gray = True
        # Number of color channels
        self.nc = 3 if not self.gray else 1
        # Image size (w/o HiRISE)
        self.bw, self.bh = 140, 140
        # default values for bbox
        self.hx, self.hy, self.hw, self.hh = 0, 0, 0.1, 0.1
        # HiRISE
        self.peak_img_sram_hirise = (
            self.pooled_img_width * self.pooled_img_height*self.nc
        )
        self.peak_img_sram_baseln = self.bw*self.bh*3
        self.bandwidth_hirise = 0
        self.bandwidth_baseln = 0
        self.avg_box_pixels_bl = 0
        self.avg_box_pixels_hr = 0
        self.num_frames = 0
        self.start_time = time.time()
        self.person_model = YOLO(self.model)

    def detect(self, ret, frame):
        if not ret:
            raise Exception("Error: Failed to capture frame.")
        frame = cv2.resize(frame, (640, 480))
        self.num_frames += 1
        frame_scaled = cv2.resize(
            frame, (self.pooled_img_width, self.pooled_img_height))
        if self.gray:
            frame_scaled = cv2.cvtColor(frame_scaled, cv2.COLOR_BGR2GRAY)
            frame_scaled = np.stack((frame_scaled,)*3, axis=-1)
        head_results_hirise = self.person_model.track(
            frame_scaled,
            verbose=False,
            persist=True,
            classes=[1],
            tracker="botsort.yaml",
            imgsz=self.pooled_img_width
        )
        frame_scaled = cv2.resize(frame, (self.bw, self.bh))
        x, y, w, h = 0, 0, 0, 0
        self.bandwidth_hirise += (
            self.pooled_img_width *
            self.pooled_img_height*self.nc
        )
        self.bandwidth_baseln += self.bw*self.bh*3
        if len(head_results_hirise[0].boxes) > 0:
            for j, headbox in reversed(
                    list(enumerate(head_results_hirise[0].boxes))):
                # Ultralytics uses X,Y,W,H bounding box coordinates (x,y are center of bbox)
                # https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format

                # Convert bbox to coordinates relative to img size
                head_relative_xywh = np.concatenate([
                    headbox.xywh.numpy()[0, :2] /
                    np.array(headbox.orig_shape)[::-1],
                    headbox.xywh.numpy()[0, 2:] /
                    np.array(headbox.orig_shape)[::-1]
                ])

                # Turn them into a list
                hx, hy, hw, hh = list(head_relative_xywh)
                peak_img_sram_hirise = max(peak_img_sram_hirise, hw*hh*3)

                graphics2d.draw_bbox_on_image(main_canvas, x+hx-w/2, y+hy-h/2, hw, hh,
                                              color=view.hirise_color if j == 0 else view.baseline_color)

                head_image_hirise = graphics2d.crop_image_by_relative_coords(
                    frame, x+hx-w/2, y+hy-h/2, hw, hh, center=True)
                head_image_baseline = graphics2d.crop_image_by_relative_coords(
                    frame_scaled, x+hx-w/2, y+hy-h/2, hw, hh, center=True)
                head_image_hirise = cv2.resize(
                    head_image_hirise, (self.pooled_img_width, self.pooled_img_height))
        self.avg_box_pixels_bl += head_image_baseline.shape[0] * \
            head_image_baseline.shape[0]*3
        self.avg_box_pixels_hr += head_image_hirise.shape[0] * \
            head_image_hirise.shape[0]*3
