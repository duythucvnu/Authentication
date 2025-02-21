from ultralytics import YOLO
import cv2

model=YOLO("face.pt")
model.export(format="openvino")
ov_model = YOLO('face_openvino_model/')
