from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("face.pt")

# Export the model to ONNX format
try:
    model.export(format="onnx")
    print("ONNX export successful!")
except Exception as e:
    print(f"ONNX export failed: {e}")