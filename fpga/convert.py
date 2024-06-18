import torch

model = torch.load('./models/face_det.pt')

torch.onnx.export(model)
