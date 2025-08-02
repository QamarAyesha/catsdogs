import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

# Title
st.title("🐱🐶 Teachable Machine Cat vs Dog Classifier")
st.markdown("Upload an image to classify it as a **Cat** or **Dog** using your Teachable Machine model.")

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model and labels
@st.cache_resource
def load_my_model():
    model = load_model("keras_Model.h5", compile=False)
    labels = [line.strip() for line in open("labels.txt", "r").readlines()]
    return model, labels

model, class_names = load_my_model()

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predict
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Display result
    st.markdown(f"### Prediction: **{class_name[2:].strip()}**")
    st.markdown(f"Confidence Score: **{confidence_score:.2%}**")

