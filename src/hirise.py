"""
"""
################################################################################
import time
import sys
import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtGui import QImage
from PySide6.QtCore import QRect
from ultralytics import YOLO
################################################################################


class HiRISE():
    def __init__(
        self,
        pooled_img_w: int = 96,
        pooled_img_h: int = 96,
        model: str = './src/models/face_det.pt',
        gray: bool = False,
        basesz: tuple = (140, 140),
        bbox_margin: float = 0.1
    ):
        self.pooled_img_width = pooled_img_w
        self.pooled_img_height = pooled_img_h
        self.model = model
        self.gray = gray
        # Number of color channels
        self.nc = 3 if not self.gray else 1
        # Image size (w/o HiRISE)
        self.bw, self.bh = basesz
        # default values for bbox
        self.hx, self.hy, self.hw, self.hh = 0, 0, 0.1, 0.1

        # HiRISE
        self.peak_img_sram_hirise = (
            self.pooled_img_width * self.pooled_img_height*self.nc
        )
        self.peak_img_sram_baseln = self.bw*self.bh*3
        self.avg_box_pixels_bl = 0
        self.avg_box_pixels_hr = 0
        self.num_frames = 0

        # YOLO Model
        self.person_model = YOLO(self.model)

        # Colors
        self.hirise_color = (141, 164, 78)
        self.baseline_color = (238, 147, 56)

        # Setup Statistics Dictionary
        self.stats = self.init_stats_dict()

    def init_stats_dict(self):
        return {
            'baseline': {
                'Peak Memory': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0
                },
                'Bandwidth': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0
                },
                'Energy': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0
                }
            },
            'hirise': {
                'Peak Memory': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0
                },
                'Bandwidth': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0
                },
                'Energy': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0
                }
            }
        }

    def draw_bbox_on_image(
            self,
            image,
            relative_x,
            relative_y,
            relative_w,
            relative_h,
            color=(0, 255, 0),
            thickness=1
    ):
        """
        Draw a bounding box on an image based on relative coordinates.

        Parameters:
            image (numpy.ndarray): Input image.
            relative_x (float): Relative x-coordinate of the top-left corner of
                the bounding box.
            relative_y (float): Relative y-coordinate of the top-left corner of
                the bounding box.
            relative_w (float): Relative width of the bounding box.
            relative_h (float): Relative height of the bounding box.
            color (tuple): Bounding box color in BGR format. Default is green.
            thickness (int): Thickness of the bounding box lines. Default is 2.
        """
        color = (color[2], color[1], color[0])
        height, width = image.shape[:2]
        x = int(relative_x * width)
        y = int(relative_y * height)
        w = int(relative_w * width)
        h = int(relative_h * height)
        x -= w//2
        y -= h//2

        # Top-left corner
        cv2.line(image, (x, y), (x, y + 10), color, thickness=thickness)
        cv2.line(image, (x, y), (x + 10, y), color, thickness=thickness)

        # Bottom-right corner
        cv2.line(image, (x + w, y), (x + w, y + 10), color, thickness=thickness)
        cv2.line(image, (x + w, y), (x + w - 10, y), color, thickness=thickness)

        # Top-right corner
        cv2.line(image, (x, y + h), (x, y + h - 10), color, thickness=thickness)
        cv2.line(image, (x, y + h), (x + 10, y + h), color, thickness=thickness)

        # Bottom-left corner
        cv2.line(image, (x + w, y + h), (x + w, y + h - 10),
                 color, thickness=thickness)
        cv2.line(image, (x + w, y + h), (x + w - 10, y + h),
                 color, thickness=thickness)

    def crop_image_by_relative_coords(
            self,
            image,
            relative_x,
            relative_y,
            relative_w,
            relative_h,
            center=False,
    ):
        """
        Crop an image based on relative coordinates.

        Parameters:
            image (numpy.ndarray): Input image.
            relative_x (float): Relative x-coordinate of the top-left corner of the crop box.
            relative_y (float): Relative y-coordinate of the top-left corner of the crop box.
            relative_w (float): Relative width of the crop box.
            relative_h (float): Relative height of the crop box.

        Returns:
            numpy.ndarray: Cropped image.
        """
        height, width = image.shape[:2]
        x = int(relative_x * width)
        y = int(relative_y * height)
        w = int(relative_w * width)
        h = int(relative_h * height)
        if center:
            x -= w//2
            y -= h//2
        return image[y:y+h, x:x+w]

    def avg(self, running_avg, now):
        return running_avg

    def update_stats(self):
        # Min computations
        self.stats['baseline']['Energy']['min'] = min(
            self.stats['baseline']['Energy']['min'],
            self.stats['baseline']['Energy']['now']
        )
        self.stats['hirise']['Energy']['min'] = min(
            self.stats['hirise']['Energy']['min'],
            self.stats['hirise']['Energy']['now']
        )
        self.stats['baseline']['Bandwidth']['min'] = min(
            self.stats['baseline']['Bandwidth']['min'],
            self.stats['baseline']['Bandwidth']['now']
        )
        self.stats['hirise']['Bandwidth']['min'] = min(
            self.stats['hirise']['Bandwidth']['min'],
            self.stats['hirise']['Bandwidth']['now']
        )
        self.stats['baseline']['Peak Memory']['min'] = min(
            self.stats['baseline']['Peak Memory']['min'],
            self.stats['baseline']['Peak Memory']['now']
        )
        self.stats['hirise']['Peak Memory']['min'] = min(
            self.stats['hirise']['Peak Memory']['min'],
            self.stats['hirise']['Peak Memory']['now']
        )
        # Max computations
        self.stats['baseline']['Energy']['max'] = max(
            self.stats['baseline']['Energy']['max'],
            self.stats['baseline']['Energy']['now']
        )
        self.stats['hirise']['Energy']['max'] = max(
            self.stats['hirise']['Energy']['max'],
            self.stats['hirise']['Energy']['now']
        )
        self.stats['baseline']['Bandwidth']['max'] = max(
            self.stats['baseline']['Bandwidth']['max'],
            self.stats['baseline']['Bandwidth']['now']
        )
        self.stats['hirise']['Bandwidth']['max'] = max(
            self.stats['hirise']['Bandwidth']['max'],
            self.stats['hirise']['Bandwidth']['now']
        )
        self.stats['baseline']['Peak Memory']['max'] = max(
            self.stats['baseline']['Peak Memory']['max'],
            self.stats['baseline']['Peak Memory']['now']
        )
        self.stats['hirise']['Peak Memory']['max'] = max(
            self.stats['hirise']['Peak Memory']['max'],
            self.stats['hirise']['Peak Memory']['now']
        )
        # Average Computations
        self.stats['baseline']['Energy']['avg'] = self.avg(
            self.stats['baseline']['Energy']['avg'],
            self.stats['baseline']['Energy']['now']
        )
        self.stats['hirise']['Energy']['avg'] = self.avg(
            self.stats['hirise']['Energy']['avg'],
            self.stats['hirise']['Energy']['now']
        )
        self.stats['baseline']['Bandwidth']['avg'] = self.avg(
            self.stats['baseline']['Bandwidth']['avg'],
            self.stats['baseline']['Bandwidth']['now']
        )
        self.stats['hirise']['Bandwidth']['avg'] = self.avg(
            self.stats['hirise']['Bandwidth']['avg'],
            self.stats['hirise']['Bandwidth']['now']
        )
        self.stats['baseline']['Peak Memory']['avg'] = self.avg(
            self.stats['baseline']['Peak Memory']['avg'],
            self.stats['baseline']['Peak Memory']['now']
        )
        self.stats['hirise']['Peak Memory']['avg'] = self.avg(
            self.stats['hirise']['Peak Memory']['avg'],
            self.stats['hirise']['Peak Memory']['now']
        )

    def detect(self, ret, frame, tab):
        bandwidth_baseln = 0.0
        bandwidth_hirise = 0.0
        head_image_baseline = None
        head_image_hirise = None
        detect_image = None
        # Resize the frame
        frame = cv2.resize(frame, (640, 480))
        # Increment frame counter
        self.num_frames += 1
        # Scale the frame
        frame_scaled = cv2.resize(
            frame, (self.pooled_img_width, self.pooled_img_height))
        # Should we convert the image to gray?
        if self.gray:
            frame_scaled = cv2.cvtColor(frame_scaled, cv2.COLOR_BGR2GRAY)
            frame_scaled = np.stack((frame_scaled,)*3, axis=-1)
        detect_image = frame_scaled.copy()
        # Track the head
        head_results_hirise = self.person_model.track(
            frame_scaled,
            verbose=False,
            persist=True,
            classes=[1],
            tracker="botsort.yaml",
            imgsz=self.pooled_img_width
        )
        # Scale image
        frame_scaled = cv2.resize(frame, (self.bw, self.bh))
        x, y, w, h = 0, 0, 0, 0

        # Bandwidth computations
        bandwidth_baseln += self.bw*self.bh*3
        bandwidth_hirise += (
            self.pooled_img_width * self.pooled_img_height * self.nc
        )
        # If we detected head boxes then iterate through
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
                peak_img_sram_hirise = max(self.peak_img_sram_hirise, hw*hh*3)

                self.draw_bbox_on_image(
                    detect_image,
                    x+hx-w/2,
                    y+hy-h/2,
                    hw,
                    hh,
                    color=self.hirise_color if j == 0 else self.baseline_color
                )
                # Returns a resized QImage and Numpy Array
                head_image_hirise = self.crop_image_by_relative_coords(
                    frame,
                    x+hx-w/2,
                    y+hy-h/2,
                    hw,
                    hh,
                    center=True,
                )
                # Returns a QImage and Numpy Array
                head_image_baseline = self.crop_image_by_relative_coords(
                    frame_scaled,
                    x+hx-w/2,
                    y+hy-h/2,
                    hw,
                    hh,
                    center=True,
                )
                zeros = np.zeros(head_image_baseline.shape, dtype=np.uint8)
                np.copyto(zeros, head_image_baseline)
                head_image_baseline = zeros
                try:
                    head_image_hirise = cv2.resize(
                        head_image_hirise, (self.pooled_img_width, self.pooled_img_height))
                except Exception as e:
                    return None, None, None, self.stats
                # Update bandwidth
                bandwidth_hirise += head_image_hirise.shape[0] * \
                    head_image_hirise.shape[0]*3
                # Update our statistics
                self.stats['baseline']['Energy']['now'] = 0.0
                self.stats['hirise']['Energy']['now'] = 0.0
                self.stats['baseline']['Bandwidth']['now'] = bandwidth_baseln
                self.stats['hirise']['Bandwidth']['now'] = bandwidth_hirise
                self.stats['baseline']['Peak Memory']['now'] = self.peak_img_sram_baseln
                self.stats['hirise']['Peak Memory']['now'] = peak_img_sram_hirise
                if tab == 'Summary':
                    self.update_stats()
        return detect_image, head_image_baseline, head_image_hirise, self.stats
