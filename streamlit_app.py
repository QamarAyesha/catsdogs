import streamlit as st
import streamlit.components.v1 as components
import json

# Class labels for your model (index must match Teachable Machine order)


# Set correct class labels (must match model training order)
class_labels = {
    0: "Cat",
    1: "Dog"
}

# Convert labels to JSON string for JavaScript
class_labels_json = json.dumps(class_labels)

# Hosted TensorFlow.js model URL
model_url = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json"

# HTML/JS code to embed in Streamlit
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
            <b>Prediction:</b> ${className}<br/>
            <b>Confidence:</b> ${(maxProb * 100).toFixed(2)}%
        `;
    }}

    document.getElementById("upload").addEventListener("change", (event) => {{
        const file = event.target.files[0];
        if (!file) return;

        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.onload = () => predictImage(img);
        img.width = 224;
        img.height = 224;

        const preview = document.getElementById("preview");
        preview.innerHTML = "";
        preview.appendChild(img);
    }});

    loadModel();
</script>
"""

# Build Streamlit app
st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")
st.title("🐱🐶 Cat vs Dog Classifier")
st.markdown("Upload an image of a cat or dog to get a prediction.")
components.html(html_code, height=600)

    0: "Cat",
    1: "Dog"
}

# Convert to JSON for JS
class_labels_json = json.dumps(class_labels)

# Your hosted model.json URL
model_url = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json"

# HTML + JS code to run the model in-browser
html_code = f"""
<div style="font-family: sans-serif;">
    <h3>Teachable Machine: Cat vs Dog Classifier</h3>
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
            <b>Prediction:</b> ${className}<br/>
            <b>Confidence:</b> ${maxProb.toFixed(2)}
        `;
    }}

    document.getElementById("upload").addEventListener("change", (event) => {{
        const file = event.target.files[0];
        if (!file) return;

        const img = document.createElement("img");
        img.src = URL.createObjectURL(file);
        img.onload = () => predictImage(img);
        img.width = 224;
        img.height = 224;

        const preview = document.getElementById("preview");
        preview.innerHTML = "";
        preview.appendChild(img);
    }});

    loadModel();
</script>
"""

# Streamlit page setup
st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")
st.title("🐱🐶 Cat vs Dog Classifier")
st.markdown("Upload an image of a cat or dog to see which one the model predicts!")
components.html(html_code, height=600)
