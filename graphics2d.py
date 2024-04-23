import numpy as np

def relative_to_absolute(relative_pos, max_size):
    relx,rely = relative_pos
    sx,sy = max_size
    return int(relx*(sx-1)), int(rely*(sy-1))

def absolute_to_relative(absolute_pos, max_size):
    px,py = absolute_pos
    sx,sy = max_size
    return px/sx, py/sy

class ViewGridElement():
    def __init__(self, name, position, size, grid, meta=None):
        self.name = name
        self.position = position
        self.x, self.y = position
        self.size = size
        self.width, self.height = size
        self.grid = grid
        self.meta = meta if not meta is None else {}

    def render(self):
        pass

class ResizeModes():
    scale = 0
    clip = 1
    def CLIP(element, canvas):
        w,h,c = canvas.shape
        if not w==element.width or h==element.height:
            arr = np.zeros((element.width, element.height, c))
            w = min(w,element.width)
            h = min(h,element.height)
            arr[:w,:h,:] = canvas[:w,:h,:]
            canvas = arr
        return canvas
    scale_modes = [None, CLIP]

class ViewGrid():
    DEFAULT_META_VALUES = {
        "resize":ResizeModes.clip
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
        element = self.canvas_elements[idx]
        return self.canvas[element.x:element.x+element.width,
                           element.y:element.y+element.height, :]

    def grid(self, coords_abs=(0,0,0,0), coords_rel=(0,0,0,0), meta=None):
        meta = ViewGrid.DEFAULT_META_VALUES if meta is None else meta

        x,y,w,h = coords_abs
        rx,ry,rw,rh = coords_rel
        x2,y2=relative_to_absolute((rx,ry), self.size)
        w2,h2=relative_to_absolute((rw,rh), self.size)
        x+=x2; y+=y2; w+=w2; h+=h2
        
        if x<0 or y<0 or x+w>=self.width or y+h>=self.height:
            raise ValueError(f"Expected (x,y), (w,h) to be in range 0<x<x+w<width, 0<y<y+h<height got ({x},{y}), ({w}, {h}), for canvas of size ({self.width}), ({self.height})")

        self.canvas_elements.append(ViewGridElement(len(self.canvas_elements),
                                                    (x,y), (w,h), self, meta=meta))
        
        return len(self.canvas_elements)-1
    
    def set(self, grid_idx, new_canvas, cv2=False):
        new_canvas = np.swapaxes(new_canvas, 0, 1) if cv2 else new_canvas
        new_canvas = new_canvas.astype(self.dtype)
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

class MainDisplay():
    def __init__(self):
        self.view = ViewGrid((1200,800))
        self.left_half_idx = self.view.grid(coords_rel=(0,0,0.8,1))
        self.right_half_idx = self.view.grid(coords_rel=(0.8,0,0.2,1))

        self.view.fill(self.left_half_idx, (255,0,0))
        self.view.fill(self.right_half_idx, (0,255,0))

    def cv2(self):
        return self.view.cv2()
    
    def update_main(self, img, cv2=True):
        self.view.set(self.left_half_idx, img, cv2=cv2)
