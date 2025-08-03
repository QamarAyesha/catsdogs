import streamlit as st
import streamlit.components.v1 as components
import json

# Set page configuration
st.set_page_config(
    page_title="Cat vs Dog Classifier",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define class labels for cats and dogs
class_labels = {
    0: "Cat",
    1: "Dog"
}

# Teachable Machine TensorFlow.js Integration with File Upload
def teachable_machine_component(class_labels):
    # Convert class_labels to JSON string
    class_labels_json = json.dumps(class_labels)
    
    # Use a multi-line string for the HTML/JavaScript code
    html_code = f"""
    <div style="font-family: sans-serif; color: var(--text-color);">Teachable Machine Image Model</div>
    <input type="file" id="file-input" accept="image/*" />
    <div id="image-container"></div>
    <div id="label-container" style="margin-top: 20px; font-size: 16px; color: var(--text-color);"></div>
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
    <script type="text/javascript">
        // Teachable Machine model URL
        const modelURL = "https://storage.googleapis.com/tm-model/B7vA7NlaK/model.json";

        // Class labels
        const classLabels = {class_labels_json};

        let model;
        let lastResult = null;

        // Load the model
        async function init() {{
            try {{
                console.log("Loading model...");
                console.log("Model URL:", modelURL);

                // Load the model using tf.loadLayersModel
                model = await tf.loadLayersModel(modelURL);
                console.log("Model loaded successfully!");

                // Set up file input listener
                const fileInput = document.getElementById("file-input");
                fileInput.addEventListener("change", handleFileUpload, false);
                
                // Initialize Streamlit component value
                if (typeof Streamlit !== "undefined" && Streamlit.setComponentValue) {{
                    Streamlit.setComponentValue({{status: "ready"}});
                }}
            }} catch (error) {{
                console.error("Error loading model:", error);
                const labelContainer = document.getElementById("label-container");
                labelContainer.innerHTML = `<div style="color: red;">Error loading model: ${{error.message}}</div>`;
                
                if (typeof Streamlit !== "undefined" && Streamlit.setComponentValue) {{
                    Streamlit.setComponentValue({{status: "error", message: error.message}});
                }}
            }}
        }}

        // Handle file upload
        async function handleFileUpload(event) {{
            const file = event.target.files[0];
            if (!file) return;

            console.log("File uploaded:", file.name);

            // Display the uploaded image
            const imageContainer = document.getElementById("image-container");
            imageContainer.innerHTML = "";
            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.width = 300;
            img.height = 300;
            img.style.borderRadius = "10px";
            img.style.boxShadow = "0 4px 8px rgba(0,0,0,0.1)";
            imageContainer.appendChild(img);

            // Wait for the image to load before making predictions
            img.onload = async () => {{
                console.log("Image loaded, making predictions...");

                // Preprocess the image
                const tensor = tf.browser.fromPixels(img)
                    .resizeNearestNeighbor([224, 224]) // Resize to 224x224
                    .toFloat() // Convert to float
                    .div(tf.scalar(255)) // Normalize to [0, 1]
                    .expandDims(); // Add batch dimension

                // Make predictions
                await predict(tensor);
            }};
        }}

        // Make predictions on the uploaded image
        async function predict(tensor) {{
            try {{
                console.log("Predicting...");
                const prediction = await model.predict(tensor);
                console.log("Raw predictions:", prediction);

                // Log the probabilities for each class
                const probabilities = await prediction.data();
                console.log("Probabilities:", probabilities);

                // Get the predicted class
                const predictedClass = tf.argMax(prediction, 1).dataSync()[0];
                const confidence = tf.max(prediction).dataSync()[0];

                // Get the class label
                const className = classLabels[predictedClass] || "Unknown Class";

                // Log the results
                console.log(`Predicted Class: ${{className}}, Confidence: ${{confidence}}`);

                // Determine if cat or dog
                const isCat = predictedClass === 0;
                const isDog = predictedClass === 1;

                // Store the result
                lastResult = {{
                    predicted_class: className,
                    confidence: confidence,
                    is_cat: isCat,
                    is_dog: isDog,
                    status: "prediction"
                }};

                // Display the results
                const labelContainer = document.getElementById("label-container");
                labelContainer.innerHTML = `
                    <div style="margin-bottom: 10px; font-size: 20px;">
                        <span style="font-weight: bold; color: var(--text-color);">Prediction:</span>
                        <span style="color: ${{isCat ? "#2196F3" : "#FF9800"}}; font-weight: bold; font-size: 24px;">
                            ${{className}} ${{isCat ? "🐱" : "🐶"}}
                        </span>
                    </div>
                    <div style="margin-bottom: 10px; font-size: 18px;">
                        <span style="font-weight: bold; color: var(--text-color);">Confidence:</span>
                        <span style="color: ${{isCat ? "#2196F3" : "#FF9800"}}; font-weight: bold;">
                            ${{(confidence * 100).toFixed(2)}}%
                        </span>
                    </div>
                    <div style="margin-top: 20px; display: flex; justify-content: center;">
                        <div style="background-color: ${{isCat ? "#2196F3" : "#FF9800"}}; 
                            color: white; padding: 10px 20px; border-radius: 25px; 
                            font-weight: bold; font-size: 20px;">
                            ${{isCat ? "Feline Friend Detected!" : "Doggo Detected!"}}
                        </div>
                    </div>
                `;

                // Send results back to Streamlit
                if (typeof Streamlit !== "undefined" && Streamlit.setComponentValue) {{
                    Streamlit.setComponentValue(lastResult);
                }} else {{
                    console.error("Streamlit API not available.");
                }}

                console.log("Predictions completed!");
            }} catch (error) {{
                console.error("Error making predictions:", error);
                const labelContainer = document.getElementById("label-container");
                labelContainer.innerHTML = `<div style="color: red;">Error making predictions: ${{error.message}}</div>`;
                
                if (typeof Streamlit !== "undefined" && Streamlit.setComponentValue) {{
                    Streamlit.setComponentValue({{status: "error", message: error.message}});
                }}
            }}
        }}

        // Initialize the model
        init();
    </script>
    <style>
        :root {{
            --text-color: black;
            --background-color: white;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --text-color: white;
                --background-color: #1e1e1e;
            }}
        }}
        body {{
            background-color: var(--background-color);
            padding: 20px;
        }}
        #file-input {{
            display: block;
            margin: 20px auto;
            padding: 10px;
            border: 2px dashed #ccc;
            border-radius: 10px;
            width: 80%;
            text-align: center;
            cursor: pointer;
        }}
        #file-input:hover {{
            border-color: #4CAF50;
            background-color: #f0fff4;
        }}
    </style>
    """

    # Render the HTML/JavaScript code
    return components.html(html_code, height=600)

# Streamlit App
def main():
    st.title("🐱🐶 Cat vs Dog Classifier")
    st.write("Upload an image to classify whether it contains a cat or a dog using our AI model.")
    
    # Columns layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("How It Works")
        st.markdown("""
        1. **Upload an image** using the file uploader
        2. Our AI model will analyze the image
        3. Results will show whether it's a cat or dog
        4. Confidence percentage indicates prediction certainty
        
        The model was trained using Google's Teachable Machine platform with thousands of cat and dog images.
        """)
        
        st.subheader("Tips for Best Results")
        st.markdown("""
        - Use clear, well-lit photos
        - Center the animal in the frame
        - Avoid images with multiple animals
        - Works best with cats and dogs (not other animals)
        """)
        
        st.markdown("""
        <div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; margin-top: 20px;">
            <h4>About the Model</h4>
            <p>This model uses a MobileNetV2 architecture trained on thousands of cat and dog images to achieve high accuracy predictions.</p>
            <p><a href="https://teachablemachine.withgoogle.com/models/B7vA7NlaK/" target="_blank">View model details</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Upload an Image")
        
        # Add Teachable Machine Component
        component_result = teachable_machine_component(class_labels)
        
        # Get the component value safely
        component_value = {}
        if component_result and isinstance(component_result, dict):
            component_value = component_result.get('value', {})
        
        # Get the status from the component
        status = component_value.get('status', 'loading')
        
        # Handle different states
        if status == 'loading':
            st.info("🔄 Loading AI model... Please wait")
        elif status == 'ready':
            st.info("ℹ️ Please upload an image to get a prediction")
        elif status == 'error':
            error_msg = component_value.get('message', 'Unknown error occurred')
            st.error(f"❌ Error: {error_msg}")
        elif status == 'prediction':
            # Display prediction results
            st.subheader("Prediction Results")
            
            if component_value.get('is_cat'):
                st.success(f"### 🐱 Cat detected with {component_value['confidence']*100:.2f}% confidence!")
            elif component_value.get('is_dog'):
                st.success(f"### 🐶 Dog detected with {component_value['confidence']*100:.2f}% confidence!")
            
            # Show confidence as a progress bar
            confidence = component_value.get('confidence', 0)
            st.progress(confidence)
            st.caption(f"Confidence level: {confidence*100:.2f}%")
            
            # Show fun facts
            if component_value.get('is_cat'):
                st.info("**Fun Fact:** Cats have 230 bones, while humans only have 206!")
            elif component_value.get('is_dog'):
                st.info("**Fun Fact:** Dogs' sense of smell is 10,000 to 100,000 times more acute than humans!")
        
        # Sample images section
        st.subheader("Try Sample Images")
        col_a, col_b = st.columns(2)
        with col_a:
            st.image("https://github.com/streamlit/example-data-cat-dog/blob/main/cat.jpg?raw=true", 
                     caption="Sample Cat", use_column_width=True)
        with col_b:
            st.image("https://github.com/streamlit/example-data-cat-dog/blob/main/dog.jpg?raw=true", 
                     caption="Sample Dog", use_column_width=True)
    
    # Footer
    st.markdown("---")
    st.caption("© 2023 Cat vs Dog Classifier | Built with Streamlit and TensorFlow.js")

if __name__ == "__main__":
    main()
