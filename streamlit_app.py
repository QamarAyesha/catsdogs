import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")

st.title("🐱🐶 Cat vs Dog Classifier")
st.markdown("Upload an image and see whether the AI predicts a **Cat** or **Dog**.")

# Teachable Machine model URL
model_url = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json"

# HTML + JavaScript code to load and predict using the model
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.9.0"></script>
</head>
<body>
  <input type="file" id="imageUpload" accept="image/*"/><br/><br/>
  <img id="preview" width="224" style="display:none; border: 1px solid #ccc;"/><br/>
  <div id="result" style="margin-top: 20px; font-size: 18px; font-weight: bold;"></div>

  <script type="text/javascript">
    const modelURL = "{model_url}";
    const labels = ["Cat", "Dog"];
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
      reader.onload = function(e) {{
        const img = document.getElementById("preview");
        img.src = e.target.result;
        img.style.display = "block";

        img.onload = async function() {{
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
            <b>Prediction:</b> ${{className}} <br/>
            <b>Confidence:</b> ${{(maxProb * 100).toFixed(2)}}%
          `;
        }}
      }};
      reader.readAsDataURL(file);
    }});
  </script>
</body>
</html>
"""

# Render the HTML component inside Streamlit
components.html(html_code, height=500)
