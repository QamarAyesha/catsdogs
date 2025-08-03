import streamlit as st
import streamlit.components.v1 as components

# Set Streamlit page config
st.set_page_config(page_title="Cat vs Dog Classifier", layout="centered")
st.title("🐱🐶 Cat vs Dog Classifier")
st.markdown("Upload an image of a **cat** or **dog**, and we'll predict the class using your Teachable Machine model.")

# Teachable Machine model URL
model_url = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json"
labels = ["Cat", "Dog"]

# Inject HTML + JS into Streamlit
html_code = f"""
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
  </head>
  <body>
    <input type="file" accept="image/*" onchange="loadImage(event)" style="margin-bottom: 20px;" />
    <br>
    <img id="preview" width="224" style="display:none;"/>
    <p id="result" style="font-size:18px;"></p>

    <script>
      let model, labels = {labels};

      async function loadModel() {{
        model = await tf.loadGraphModel("{model_url}");
        console.log("Model loaded");
      }}

      async function predictImage(img) {{
        const tensor = tf.browser.fromPixels(img)
            .resizeNearestNeighbor([224, 224])
            .toFloat()
            .expandDims();

        const prediction = await model.predict(tensor).data();
        const maxProb = Math.max(...prediction);
        const predictedIndex = prediction.indexOf(maxProb);
        const className = labels[predictedIndex];

        document.getElementById("result").innerHTML = `
          <b>Prediction:</b> {{className}} <br/>
          <b>Confidence:</b> {{(maxProb * 100).toFixed(2)}}%
        `;
      }}

      function loadImage(event) {{
        const file = event.target.files[0];
        if (!file) return;

        const img = document.getElementById("preview");
        img.src = URL.createObjectURL(file);
        img.style.display = "block";
        img.onload = () => predictImage(img);
      }}

      loadModel();
    </script>
  </body>
</html>
"""

# Render the custom HTML + JS component
components.html(html_code, height=600)
