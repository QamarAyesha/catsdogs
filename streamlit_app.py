import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")
st.title("🐱🐶 Upload Image: Cat or Dog?")

# HTML + JS for image upload-based classification
components.html(
    """
    <style>
        #label-container div {
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 1rem;
        }
    </style>

    <input type="file" id="upload-image" accept="image/*"/>
    <br><br>
    <img id="uploaded-image" width="224"/>
    <div id="label-container"></div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest"></script>
    <script type="text/javascript">
        const URL = "https://teachablemachine.withgoogle.com/models/B7vA7NlaK/";
        let model, maxPredictions;

        const fileInput = document.getElementById("upload-image");
        const imgTag = document.getElementById("uploaded-image");
        const labelContainer = document.getElementById("label-container");

        async function loadModel() {
            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";
            model = await tmImage.load(modelURL, metadataURL);
            maxPredictions = model.getTotalClasses();
        }

        async function predictImage(image) {
            const prediction = await model.predict(image);
            labelContainer.innerHTML = "";
            for (let i = 0; i < maxPredictions; i++) {
                const p = prediction[i];
                const label = document.createElement("div");
                label.innerText = `${p.className}: ${(p.probability * 100).toFixed(2)}%`;
                labelContainer.appendChild(label);
            }
        }

        fileInput.addEventListener("change", async function() {
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imgTag.src = e.target.result;
                    imgTag.onload = async function() {
                        await loadModel();
                        await predictImage(imgTag);
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    </script>
    """,
    height=600,
)


