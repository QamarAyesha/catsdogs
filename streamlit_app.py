import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")
st.title("🐱🐶 Upload an Image to See Prediction")

components.html(
    """
    <div style="text-align:center;">
        <input type="file" id="imageUpload" accept="image/*"/><br><br>
        <img id="imagePreview" width="224" style="display:none;"/>
        <div id="label-container" style="margin-top: 20px;"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/@teachablemachine/image@latest"></script>
    <script type="text/javascript">
        const URL = "https://teachablemachine.withgoogle.com/models/B7vA7NlaK/";
        let model, maxPredictions;

        async function loadModel() {
            const modelURL = URL + "model.json";
            const metadataURL = URL + "metadata.json";
            model = await tmImage.load(modelURL, metadataURL);
            maxPredictions = model.getTotalClasses();
        }

        async function predictImage(imageElement) {
            const prediction = await model.predict(imageElement);
            const labelContainer = document.getElementById("label-container");
            labelContainer.innerHTML = "";  // clear previous
            prediction.forEach(p => {
                const label = document.createElement("div");
                label.style.fontSize = "18px";
                label.style.fontWeight = "bold";
                label.textContent = `${p.className}: ${(p.probability * 100).toFixed(2)}%`;
                labelContainer.appendChild(label);
            });
        }

        loadModel();

        document.getElementById("imageUpload").addEventListener("change", function(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.getElementById("imagePreview");
                img.src = e.target.result;
                img.style.display = "block";
                img.onload = () => predictImage(img);
            };
            reader.readAsDataURL(file);
        });
    </script>
    """,
    height=700,
)

