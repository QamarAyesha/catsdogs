import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("model/keras_model.h5")
    return model

model = load_model()

# App title and description
st.title("🐾 Cat vs Dog Classifier")
st.markdown("Upload an image and let the AI predict whether it's a **cat** or a **dog**.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess image (match model input shape)
    img_size = (224, 224)  # Update based on your model’s input size
    img = image.resize(img_size)
    img_array = tf.keras.utils.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Model expects batch dimension

    # Predict
    prediction = model.predict(img_array)[0][0]  # Assuming binary output

    # Display result
    label = "🐶 Dog" if prediction > 0.5 else "🐱 Cat"
    confidence = prediction if prediction > 0.5 else 1 - prediction
    st.markdown(f"### Prediction: **{label}**")
    st.markdown(f"Confidence: **{confidence:.2%}**")
