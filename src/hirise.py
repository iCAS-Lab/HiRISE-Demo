"""
"""
################################################################################
import time
import sys
import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal
from ultralytics import YOLO
################################################################################


class HiRISE(QObject):

    update_num_heads = Signal(int)

    def __init__(
        self,
        pooled_img_w: int = 32,
        pooled_img_h: int = 32,
        # model: str = './src/models/face_det.pt',
        model: str = './src/models/face_det_full_integer_quant_edgetpu.tflite',
        gray: bool = False,
        basesz: tuple = (96, 96),
    ):
        super().__init__()
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
        self.peak_img_sram_hirise = float(
            self.pooled_img_width * self.pooled_img_height*self.nc
        )
        self.peak_img_sram_baseln = self.bw*self.bh*3
        self.avg_box_pixels_bl = 0
        self.avg_box_pixels_hr = 0
        self.num_frames = 0

        # YOLO Model
        self.person_model = YOLO(self.model, task='detect')

        # Colors
        self.hirise_color = (141, 164, 78)
        self.baseline_color = (238, 147, 56)

        # Original Image Size
        self.camera_image_size = (96, 96)
        self.hirise_pixel_array_size = (96, 96)
        self.camera_image_sizes = {
            0: (96, 96),
            1: (100, 100),
            2: (128, 128),
            3: (256, 256),
            4: (320, 320),
            5: (640, 360),
            6: (640, 480),
            7: (800, 600),
            8: (960, 540),
            9: (960, 720),
            10: (1024, 576),
            11: (1280, 720),
            12: (1280, 960),
            13: (1920, 1080),
            14: (2560, 1440),
            15: (3840, 2160)
        }
        self.baseline_array_sizes = {
            0: (96, 96),
            1: (100, 100),
            2: (128, 128),
            3: (256, 256),
            4: (320, 320),
            5: (640, 360),
            6: (640, 480),
            7: (800, 600),
            8: (960, 540),
            9: (960, 720),
            10: (1024, 576),
            11: (1280, 720),
            12: (1280, 960),
            13: (1920, 1080),
            14: (2560, 1440),
            15: (3840, 2160)
        }

        self.hirise_array_sizes = {
            0: (96, 96),
            1: (100, 100),
            2: (128, 128),
            3: (256, 256),
            4: (320, 320),
            5: (640, 360),
            6: (640, 480),
            7: (800, 600),
            8: (960, 540),
            9: (960, 720),
            10: (1024, 576),
            11: (1280, 720),
            12: (1280, 960),
            13: (1920, 1080),
            14: (2560, 1440),
            15: (3840, 2160)
        }
        self.detect_sizes = {}
        for i in range(16):
            self.detect_sizes[i] = (i+1)*32

        # Constant Baseline Computations, divide by 1000 for kB
        self.bandwidth_baseln = float(self.camera_image_size[0] *
                                      self.camera_image_size[1] * 3) / 1000
        self.c_bandwidth_baseln = (self.bw*self.bh*3.0) / 1000
        self.peak_memory_baseln = float(self.camera_image_size[0] *
                                        self.camera_image_size[1] * 3) / 1000
        self.c_peak_memory_baseln = (self.bw*self.bh*3.0) / 1000

        # Running Values for averaging
        self.total_latency = 0.0
        self.total_fps = 0.0
        self.total_hirise_bandwidth = 0.0
        self.total_hirise_peak_memory = 0.0

        # Focus
        self.focus_number = 0
        self.num_heads = 0

        # Setup Statistics Dictionary
        self.init_stats_dict()

    def reset_values(self):
        self.bandwidth_baseln = float(self.camera_image_size[0] *
                                      self.camera_image_size[1] * 3) / 1000
        self.c_bandwidth_baseln = (self.bw*self.bh*3.0) / 1000
        self.peak_memory_baseln = float(self.camera_image_size[0] *
                                        self.camera_image_size[1] * 3) / 1000
        self.c_peak_memory_baseln = (self.bw*self.bh*3.0) / 1000
        self.total_latency = 0.0
        self.total_fps = 0.0
        self.total_hirise_bandwidth = 0.0
        self.total_hirise_peak_memory = 0.0
        self.num_frames = 0
        self.init_stats_dict()

    def change_camera_resolution(self, id: int):
        self.camera_image_size = self.camera_images_size[id]
        self.reset_values()
        return self.camera_image_size

    def change_baseline_array(self, id: int):
        self.bw, self.bh = self.baseline_array_sizes[id]
        self.reset_values()
        return self.baseline_array_sizes[id]

    def change_hirise_array(self, id: int):
        self.hirise_pixel_array_size = self.hirise_array_sizes[id]
        self.reset_values()
        return self.hirise_pixel_array_size

    def change_detection_resolution(self, id: int):
        self.pooled_img_height = self.detect_sizes[id]
        self.pooled_img_width = self.detect_sizes[id]
        self.reset_values()
        return self.detect_sizes[id]

    def init_stats_dict(self):
        self.stats = {
            'baseline': {
                'Peak Memory': {
                    'now': self.peak_memory_baseln,
                    'min': self.peak_memory_baseln,
                    'max': self.peak_memory_baseln,
                    'avg': self.peak_memory_baseln,
                    'c_now': self.c_peak_memory_baseln,
                    'c_min': self.c_peak_memory_baseln,
                    'c_max': self.c_peak_memory_baseln,
                    'c_avg': self.c_peak_memory_baseln
                },
                'Bandwidth': {
                    'now': self.bandwidth_baseln,
                    'min': self.bandwidth_baseln,
                    'max': self.bandwidth_baseln,
                    'avg': self.bandwidth_baseln,
                    'c_now': self.c_bandwidth_baseln,
                    'c_min': self.c_bandwidth_baseln,
                    'c_max': self.c_bandwidth_baseln,
                    'c_avg': self.c_bandwidth_baseln
                }
            },
            'hirise': {
                'Peak Memory': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0,
                    'units': 'kilobytes'
                },
                'Bandwidth': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0,
                    'units': 'kilobytes'
                },
                'Latency': {
                    'now': 0.0,
                    'min': np.inf,
                    'max': -np.inf,
                    'avg': 0.0,
                    'fps_now': 0.0,
                    'fps_min': np.inf,
                    'fps_max': -np.inf,
                    'fps_avg': 0.0,
                    'units': 'milliseconds'
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

    def avg(self, running_total, now):
        return running_total

    def update_stats(self):
        self.stats['hirise']['Latency']['fps_now'] = (
            1000 / self.stats['hirise']['Latency']['now']
        )
        # Min computations
        self.stats['hirise']['Latency']['min'] = min(
            self.stats['hirise']['Latency']['min'],
            self.stats['hirise']['Latency']['now']
        )
        self.stats['hirise']['Latency']['fps_min'] = min(
            self.stats['hirise']['Latency']['fps_min'],
            self.stats['hirise']['Latency']['fps_now']
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
        self.stats['hirise']['Latency']['max'] = max(
            self.stats['hirise']['Latency']['max'],
            self.stats['hirise']['Latency']['now']
        )
        self.stats['hirise']['Latency']['fps_max'] = max(
            self.stats['hirise']['Latency']['fps_max'],
            self.stats['hirise']['Latency']['fps_now']
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
        self.total_latency += self.stats['hirise']['Latency']['now']
        self.total_fps += self.stats['hirise']['Latency']['fps_now']
        self.total_hirise_peak_memory += self.stats['hirise']['Peak Memory']['now']
        self.total_hirise_bandwidth += self.stats['hirise']['Bandwidth']['now']
        self.stats['hirise']['Latency']['avg'] = (
            self.total_latency / self.num_frames
        )
        self.stats['hirise']['Latency']['fps_avg'] = (
            self.total_fps / self.num_frames
        )
        self.stats['hirise']['Peak Memory']['avg'] = (
            self.total_hirise_peak_memory / self.num_frames
        )
        self.stats['hirise']['Bandwidth']['avg'] = (
            self.total_hirise_bandwidth / self.num_frames
        )

    def detect(self, ret, frame, tab):
        bandwidth_hirise = 0.0
        peak_img_sram_hirise = (self.pooled_img_width *
                                self.pooled_img_height*self.nc)  # HiRISE
        head_image_baseline = None
        head_image_hirise = None
        detect_image = None
        # Resize the frame, this is the camera's default resolution
        frame = cv2.resize(frame, self.camera_image_size)
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
            cv2.resize(frame_scaled, (96, 96)),
            verbose=False,
            persist=True,
            classes=[1],
            tracker="botsort.yaml",
            imgsz=96
        )

        latency = np.sum(list(head_results_hirise[0].speed.values()))
        # Scale image
        frame_scaled = cv2.resize(frame, (self.bw, self.bh))
        # frame_scaled = frame.copy()
        x, y, w, h = 0, 0, 0, 0

        # Bandwidth computations
        bandwidth_hirise += (
            self.pooled_img_width * self.pooled_img_height * self.nc
        )
        # If we detected head boxes then iterate through
        if len(head_results_hirise[0].boxes) > 0:
            num_heads = head_results_hirise[0].boxes.id
            if num_heads is None:
                self.num_heads = 0
                self.update_num_heads.emit(self.num_heads)
            elif len(num_heads) != self.num_heads:
                # if len(num_heads) < self.num_heads and self.focus_number == self.num_heads - 1:
                #     self.focus_number -= 1
                self.num_heads = len(num_heads)
                self.update_num_heads.emit(self.num_heads)
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
                peak_img_sram_hirise = max(self.peak_img_sram_hirise, hw*hh*3.0)

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
                # Fix C-contiguous memory issues
                zeros = np.zeros(head_image_baseline.shape, dtype=np.uint8)
                np.copyto(zeros, head_image_baseline)
                head_image_baseline = zeros
                zeros_hirise = np.zeros(
                    head_image_hirise.shape, dtype=np.uint8)
                np.copyto(zeros_hirise, head_image_hirise)
                head_image_hirise = zeros_hirise
                # Update bandwidth
                bandwidth_hirise += head_image_hirise.shape[0] * \
                    head_image_hirise.shape[1]*3
                # Set the head to focus on if there are multiple
                if j == self.focus_number:
                    self.focus_head_hirise = head_image_hirise
                    self.focus_head_baseline = head_image_baseline
            # Update our statistics
            self.stats['hirise']['Latency']['now'] = latency
            self.stats['hirise']['Bandwidth']['now'] = bandwidth_hirise / 1000
            self.stats['hirise']['Peak Memory']['now'] = peak_img_sram_hirise / 1000
            if tab == 'Summary':
                # Increment frame counter for average calculations
                self.num_frames += 1
                self.update_stats()
        # Reset to prevent overflow when running for long durations
        if self.num_frames > 1000:
            print(f'LOG --> RESET FRAME COUNTER...')
            self.num_frames = 0
            self.total_hirise_bandwidth = 0.0
            self.total_hirise_peak_memory = 0.0
            self.total_latency = 0.0
            self.total_fps = 0.0
        return detect_image, self.focus_head_baseline, self.focus_head_hirise, self.stats
