import streamlit as st
import streamlit.components.v1 as components
import json

# Class labels from your model
class_labels = {
    0: "Cat",
    1: "Dog"
}

def teachable_machine_component(class_labels):
    class_labels_json = json.dumps(class_labels)

    html_code = f"""
    <div style="font-family: sans-serif;">Cat vs Dog Classifier</div>
    <input type="file" id="file-input" accept="image/*" />
    <div id="image-container"></div>
    <div id="label-container" style="margin-top: 20px; font-size: 16px;"></div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
    <script type="text/javascript">
        const modelURL = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json";
        const classLabels = {class_labels_json};
        let model;

        async function init() {{
            try {{
                model = await tf.loadGraphModel(modelURL);
                document.getElementById("file-input").addEventListener("change", handleFileUpload, false);
            }} catch (error) {{
                document.getElementById("label-container").innerHTML = "<div style='color:red;'>Error loading model: " + error.message + "</div>";
            }}
        }}

        async function handleFileUpload(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.width = 224;
            img.height = 224;

            const container = document.getElementById("image-container");
            container.innerHTML = "";
            container.appendChild(img);

            img.onload = async () => {{
                const tensor = tf.browser.fromPixels(img)
                    .resizeNearestNeighbor([224, 224])
                    .toFloat()
                    .div(tf.scalar(255))
                    .expandDims();

                const prediction = await model.predict(tensor);
                const probs = await prediction.data();
                const maxIdx = probs.indexOf(Math.max(...probs));
                const className = classLabels[maxIdx];
                const confidence = (probs[maxIdx] * 100).toFixed(2);

                document.getElementById("label-container").innerHTML = `
                    <div><strong>Prediction:</strong> ${className}</div>
                    <div><strong>Confidence:</strong> ${confidence}%</div>
                `;
            }};
        }}

        init();
    </script>
    """
    components.html(html_code, height=500)

# Streamlit App Entry
def main():
    st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")
    st.title("🐾 Cat vs Dog Classifier")
    st.write("Upload an image and the model will predict if it's a **Cat** or **Dog**.")

    teachable_machine_component(class_labels)

if __name__ == "__main__":
    main()
