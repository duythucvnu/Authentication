from ultralytics import YOLO
import streamlit as st
import cv2
import settings
import face_recognition
import app


def app():
    i=1
def load_model(model_path):
    model = YOLO(model_path)
    return model
def play_webcam(conf, model, file_path):

    source_webcam = settings.WEBCAM_PATH
    img = cv2.imread(file_path) 
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_encoding = face_recognition.face_encodings(rgb_img)[0]  # Pass face locations
    
    try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                ret, frame = vid_cap.read()
                if ret:
                    img2 = frame
                    p=0
                    rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

                    # **Check if a face is found in the webcam frame**
                    face_locations2 = face_recognition.face_locations(rgb_img2)
                    if not face_locations2:
                        status = "No Match"  # Or handle the no-face case as needed
                        img_encoding2 = None  # Set encoding to None when no face is detected
                    else:
                        img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]  # Pass face locations
                        match = face_recognition.compare_faces([img_encoding], img_encoding2)
                        if bool(match[0]) == True: # Check if match[0] is True.  `compare_faces` returns a list.
                            status = "Match"
                        else:
                            status = "No Match"

                    results = model.predict(frame, conf=conf)
                    for result in results:
                        for detection in result.boxes:  # Each detection is a bounding box
                            # Extract class ID and label
                            class_id = int(detection.cls)
                            label = "Real" if class_id == 1 else "Fake"
                            if class_id == 0:
                                p-=10
                            else:
                                p+=1
                            # Extract bounding box coordinates
                            bbox = detection.xyxy[0].tolist()  # [x_min, y_min, x_max, y_max]
                            x_min, y_min, x_max, y_max = map(int, bbox)  # Convert to integers
                            
                            # Draw bounding box
                            color = (0, 255, 0) if class_id == 1 else (0, 0, 255)  # Green for "Real", Red for "Fake"
                            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)  # 2 = thickness
                            
                            # Add label text
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            font_scale = 1
                            thickness = 2
                            text = f"{label}"
                            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                            text_x = x_min
                            text_y = y_min - 10 if y_min - 10 > 10 else y_min + 10  # Adjust if too close to the top
        
                            
                            # Put text label
                            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 0) if class_id == 1 else (0, 0, 255), thickness)

                    cv2.putText(frame, f"Status: {status}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 255, 0) if status == "Match" else (0, 0, 255), 2)


                    st_frame.image(frame,
                        caption='Detected Video',
                        channels="BGR",
                        use_container_width=False
                        )
               
                    if p>0 and status == "Match":
                        st.button('Proceed', on_click = app)
                        st.stop()
                        break
                        
                else:
                    vid_cap.release()
                    break

    except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))