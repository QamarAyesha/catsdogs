import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os

st.set_page_config(page_title="Cat vs Dog Classifier", page_icon="🐾", layout="centered")
st.title("🐱🐶 Cat vs Dog Classifier")
st.markdown("Upload an image and let the AI classify it using your Teachable Machine model!")

np.set_printoptions(suppress=True)

@st.cache_resource
def load_my_model():
    if not os.path.exists("keras_model.h5"):
        st.error("❌ 'keras_model.h5' not found.")
        st.stop()
    if not os.path.exists("labels.txt"):
        st.error("❌ 'labels.txt' not found.")
        st.stop()

    model = load_model("keras_model.h5", compile=False)
    
    # Read raw labels like "0 Class 1" → ["Class 1", "Class 2"]
    raw_labels = [line.strip().split(" ", 1)[1] for line in open("labels.txt").readlines()]
    
    # Manually remap these to real class names
    label_map = {
        "Class 1": "Cat",
        "Class 2": "Dog"
    }
    class_names = [label_map.get(label, label) for label in raw_labels]
    
    return model, class_names

model, class_names = load_my_model()

uploaded_file = st.file_uploader("Upload an image 🖼️", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📸 Uploaded Image", use_column_width=True)

    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    st.markdown(f"### ✅ Prediction: **{class_name}**")
    st.markdown(f"Confidence: **{confidence_score:.2%}**")

