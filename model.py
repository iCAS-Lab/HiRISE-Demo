
import os

import tensorflow as tf
import numpy as np
import torch
import cv2
import torch.nn.functional as F
import numpy as np
import numpy as np

class TFLite():
    def __init__(self, path, labels=None, anchors="models/hand_detect/anchors.npy"):
        self.path = path
        self.interpreter = tf.lite.Interpreter(model_path=path)
        self.interpreter.allocate_tensors()
        self.input_shape = self.interpreter.get_input_details()[0]['shape']
        self.width, self.height = self.input_shape[1], self.input_shape[2]
        self.labels = labels
        self.anchors = np.load(anchors)
        print("Loaded TFLite with input shape: ", self.input_shape)

    def __call__(self, input):
        input = cv2.resize(input, (self.height, self.width))
        if len(input.shape) < len(self.input_shape):
            input = np.expand_dims(input, 0)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        # Set input tensor
        input = input.astype(input_details[0]['dtype'])/255
        self.interpreter.set_tensor(input_details[0]['index'], input)

        # Run inference
        self.interpreter.invoke()

        # Get output tensor
        regressors = self.interpreter.get_tensor(output_details[0]['index'])[0]
        classificators = self.interpreter.get_tensor(output_details[1]['index'])[0,:,0]
        
        return output_data