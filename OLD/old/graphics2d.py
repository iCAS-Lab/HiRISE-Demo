import numpy as np
import cv2
import copy

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

def relative_to_absolute(relative_pos, max_size):
    relx,rely = relative_pos
    sx,sy = max_size
    return int(relx*(sx-1)), int(rely*(sy-1))

def absolute_to_relative(absolute_pos, max_size):
    px,py = absolute_pos
    sx,sy = max_size
    return px/sx, py/sy

def draw_bbox_on_image(image, relative_x, relative_y, relative_w, relative_h, color=(0, 255, 0), thickness=4):
    """
    Draw a bounding box on an image based on relative coordinates.

    Parameters:
        image (numpy.ndarray): Input image.
        relative_x (float): Relative x-coordinate of the top-left corner of the bounding box.
        relative_y (float): Relative y-coordinate of the top-left corner of the bounding box.
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
    x-=w//2
    y-=h//2

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
    cv2.line(image, (x + w, y + h), (x + w, y + h - 10), color, thickness=thickness)
    cv2.line(image, (x + w, y + h), (x + w - 10, y + h), color, thickness=thickness)

def crop_image_by_relative_coords(image, relative_x, relative_y, relative_w, relative_h, center=False):
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
        x-=w//2
        y-=h//2
    return image[y:y+h, x:x+w]

def resize_with_aspect_ratio(image, target_width=None, target_height=None):
    """
    Resize the image while preserving the aspect ratio.

    Parameters:
        image (numpy.ndarray): Input image.
        target_width (int): Target width for resizing.
        target_height (int): Target height for resizing.

    Returns:
        numpy.ndarray: Resized image.
    """
    if target_width is None and target_height is None:
        raise ValueError("At least one of target_width or target_height must be provided.")

    if target_width is None:
        ratio = target_height / float(image.shape[0])
        target_width = int(image.shape[1] * ratio)
    elif target_height is None:
        ratio = target_width / float(image.shape[1])
        target_height = int(image.shape[0] * ratio)

    return cv2.resize(image, (target_width, target_height), cv2.INTER_NEAREST)

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    cv2.putText(annotated_image, f"{handedness[0].category_name}",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

class ViewGridElement():
    def __init__(self, name, position, size, grid, meta):
        self.name = name
        self.border_px = meta["border"]["width"]
        self.border_color = meta["border"]["color"]
        self.x, self.y = position
        self.width, self.height = size
        self.position = (self.x, self.y)
        self.size = (self.width, self.height)
        self.grid = grid
        self.meta = meta


    def render(self):
        self.grid.fill(self.name, self.border_color)
        self.x+=self.border_px
        self.y+=self.border_px
        self.width-=self.border_px*2
        self.height-=self.border_px*2

class ResizeModes():
    scale = 0
    clip = 1
    def SCALE(element, canvas):
        w,h,c = canvas.shape
        canvas = cv2.resize(canvas, (element.height, element.width))
        return canvas
    
    def CLIP(element, canvas):
        print(canvas.shape)
        w,h,c = canvas.shape
        arr = np.zeros((element.width, element.height, c))
        w = min(w,element.width)
        h = min(h,element.height)
        arr[:w,:h,:] = canvas[:w,:h,:]
        canvas = arr
        return canvas
    scale_modes = [SCALE, CLIP]

class ViewGrid():
    DEFAULT_META_VALUES = {
        "resize":ResizeModes.scale,
        "border":{
            "color":(255,255,255),
            "width":2,
        }
    }
    def __init__(self, size, channels=3, dtype=np.uint8):
        self.size = size
        self.width, self.height = size
        self.channels = channels
        self.dtype = dtype
        self.canvas = np.zeros((self.width, self.height, self.channels), dtype=self.dtype)
        self.canvas_elements = []

    def cv2(self):
        return np.swapaxes(self.canvas,0,1)
    
    def get(self, idx):
        if idx < -len(self.canvas_elements) or idx >= len(self.canvas_elements):
            raise IndexError(f"Canvas element out of bound for index {idx} with canvas of length {len(self.canvas_elements)}")
        return self.canvas_elements[idx]
    
    def numpy(self, idx):
        element = self.get(idx)
        arr = copy.deepcopy((self.canvas[element.x:element.x+element.width,
                           element.y:element.y+element.height, :]))
        return np.swapaxes(arr, 0, 1)

    def grid(self, coords_abs=(0,0,0,0), coords_rel=(0,0,0,0), meta=None):
        meta = ViewGrid.DEFAULT_META_VALUES if meta is None else meta

        x,y,w,h = coords_abs
        rx,ry,rw,rh = coords_rel
        x2,y2=relative_to_absolute((rx,ry), self.size)
        w2,h2=relative_to_absolute((rw,rh), self.size)
        x+=x2; y+=y2; w+=w2; h+=h2
        
        if x<0 or y<0 or x+w>=self.width or y+h>=self.height:
            raise ValueError(f"Expected (x,y), (w,h) to be in range 0<x<x+w<width, 0<y<y+h<height got ({x},{y}), ({w}, {h}), for canvas of size ({self.width}), ({self.height})")

        element = ViewGridElement(len(self.canvas_elements), (x,y), (w,h), self, meta=meta)
        self.canvas_elements.append(element)
        element.render()
        
        return len(self.canvas_elements)-1
    
    def set(self, grid_idx, new_canvas, cv2=False):
        new_canvas = np.swapaxes(new_canvas, 0, 1) if cv2 else new_canvas
        new_canvas = new_canvas.astype(self.dtype)
        if new_canvas.shape[0] <= 0 or new_canvas.shape[1] <= 0:
            new_canvas = np.zeros((1,1,3))
        element = self.canvas_elements[grid_idx]
        new_canvas = ResizeModes.scale_modes[element.meta["resize"]](element, new_canvas)
        self.canvas[element.x:element.x+element.width,
                    element.y:element.y+element.height, :] = new_canvas
        
    def fill(self, grid_idx, color=(255,255,255)):
        element = self.canvas_elements[grid_idx]
        new_canvas = np.ones((element.width, element.height, len(color)))*np.array(list(color)[::-1]).astype(self.dtype)
        self.canvas[element.x:element.x+element.width,
                    element.y:element.y+element.height, :] = new_canvas

    def render(self):
        for element in self.canvas_elements:
            element.render()

    def draw_text(self, grid_idx, text, font_color=(255, 255, 255), font_scale=0.75):
        # Choose font, scale, and color
        image = self.numpy(grid_idx).copy()
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Calculate text size
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness=2)

        # Calculate text position
        text_x = (image.shape[1] - text_size[0]) // 2
        text_y = (image.shape[0] + text_size[1]) // 2

        # Draw text on the image
        cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, thickness=2)
        self.set(grid_idx, image, cv2=True)


class MainDisplay():
    def __init__(self):
        self.view = ViewGrid((1280,720))
        self.left_half_idx = self.view.grid(coords_rel=(0,0,0.8,1))
        self.hirise_img = self.view.grid(coords_rel=(0.8,0,0.2,0.5), coords_abs=(0,80,0,-80))
        self.baseline_img = self.view.grid(coords_rel=(0.8,0.5,0.2,0.5), coords_abs=(0,80,0,-80))

        self.hirise_caption = self.view.grid(coords_rel=(0.8,0,0.2,0), coords_abs=(0,0,0,80))
        self.baseline_caption = self.view.grid(coords_rel=(0.8,0.5,0.2,0), coords_abs=(0,0,0,80))

        self.hirise_color = (141,164,78)
        self.baseline_color = (238,147,56)

        self.view.fill(self.left_half_idx, (255,0,0))
        self.view.fill(self.hirise_img, (0,255,0))
        self.view.fill(self.baseline_img, (0,255,255))
        self.view.fill(self.hirise_caption, (141,164,78))
        self.view.fill(self.baseline_caption, (238,147,56))

        self.view.draw_text(self.hirise_caption, "HiRISE: Enabled")
        self.view.draw_text(self.baseline_caption, "HiRISE: Disabled")

    def cv2(self):
        return self.view.cv2()
    
    def update_hirise(self, img, cv2=True):
        self.view.set(self.hirise_img, img, cv2=cv2)
    
    def update_baseline(self, img, cv2=True):
        self.view.set(self.baseline_img, img, cv2=cv2)
    
    def update_main(self, img, cv2=True):
        self.view.set(self.left_half_idx, img, cv2=cv2)

    def get_main_canvas(self):
        return self.view.numpy(self.left_half_idx)