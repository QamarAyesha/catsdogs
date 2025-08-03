import streamlit as st
import streamlit.components.v1 as components
import json

# ✅ Class labels must match model's class order (Teachable Machine)
class_labels = {
    0: "Cat",
    1: "Dog"
}

# Convert to JSON string for use in JavaScript
class_labels_json = json.dumps(class_labels)

# ✅ Hosted model.json URL
model_url = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json"

# HTML + JS for TensorFlow.js in-browser prediction
html_code = f"""
<div style="font-family: sans-serif;">
    <h3>🐾 Teachable Machine: Cat vs Dog Classifier</h3>
    <input type="file" id="upload" accept="image/*" />
    <div id="preview" style="margin-top: 10px;"></div>
    <div id="result" style="margin-top: 20px; font-size: 18px;"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
<script type="text/javascript">
    const modelURL = "{model_url}";
    const labels = {class_labels_json};

    let model;

    async function loadModel() {{
        model = await tf.loadLayersModel(modelURL);
        console.log("Model loaded.");
    }}

    async function predictImage(imageElement) {{
        const tensor = tf.browser.fromPixels(imageElement)
            .resizeNearestNeighbor([224, 224])
            .toFloat()
            .div(tf.scalar(255.0))
            .expandDims();

        const prediction = await model.predict(tensor);
        const probs = await prediction.data();

        const maxProb = Math.max(...probs);
        const predictedIndex = probs.indexOf(maxProb);
        const className = labels[predictedIndex];

        document.getElementById("result").innerHTML = `
            <b>Prediction:</b> ${classNa
