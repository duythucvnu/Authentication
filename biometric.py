# Python In-built packages
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import settings
import helper



def authentication(file_path):
    st.title("Biometric Authentication")

    # Model type
    model_path = Path(settings.FACE)
    confidence = 0.85

    # Load Pre-trained ML Model
    try:
        model = helper.load_model(model_path)
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

    source_radio = helper.play_webcam(confidence, model, file_path)