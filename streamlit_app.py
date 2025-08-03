import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")

st.title("🐱🐶 Cat vs Dog Classifier")
st.write("Upload an image and let the Teachable Machine model tell you if it's a cat or dog!")

# Define the model URL
model_url = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json"

# Class labels (index 0 = Cat, index 1 = Dog)
class_labels = {
    0: "Cat",
    1: "Dog"
}

# JavaScript + HTML interface
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.9.0"></script>
</head>
<body>
  <input type="file" id="imageUpload" accept="image/*"/><br/><br/>
  <img id="preview" src="" width="224" style="display:none;"/><br/>
  <div id="result" style="font-size: 20px; font-weight: bold;"></div>

  <script type="text/javascript">
    const modelURL = "{model_url}";
    const labels = {list(class_labels.values())};

    let model;

    async function loadModel() {{
      model = await tf.loadGraphModel(modelURL);
      console.log("Model loaded");
    }}

    loadModel();

    document.getElementById("imageUpload").addEventListener("change", async function(event) {{
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = async function(e) {{
        const img = document.getElementById("preview");
        img.src = e.target.result;
        img.onload = async function() {{
          img.style.display = "block";

          const tensor = tf.browser.fromPixels(img)
            .resizeNearestNeighbor([224, 224])
            .toFloat()
            .div(255.0)
            .expandDims();

          const predictions = await model.predict(tensor).data();
          const maxProb = Math.max(...predictions);
          const predictedIndex = predictions.indexOf(maxProb);
          const className = labels[predictedIndex];

          document.getElementById("result").innerHTML = `
            <b>Prediction:</b> ${{className}}<br/>
            <b>Confidence:</b> ${{(maxProb * 100).toFixed(2)}}%
          `;
        }};
      }};
      reader.readAsDataURL(file);
    }});
  </script>
</body>
</html>
"""

# Render the component in Streamlit
components.html(html_code, height=400)
