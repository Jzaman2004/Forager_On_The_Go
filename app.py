import os
from flask import Flask, render_template, redirect, request, jsonify  # Added render_template
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import keras
from PIL import Image, ImageEnhance
from groq import Groq

# Force TensorFlow to use only the CPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Initialize Flask app
app = Flask(__name__, template_folder=os.path.abspath('.'))


# Define the upload folder
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load ResNet50 pre-trained model
model = tf.keras.applications.ResNet50(weights='imagenet')

# Set API key for Groq
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Function to make prediction
def predict_and_get_details(img_path):
    img = keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded_predictions = tf.keras.applications.resnet50.decode_predictions(predictions, top=1)[0]
    label, description, score = decoded_predictions[0]
    
    return description, score, img

# Function to modify the image slightly (color enhancement, rotation)
def modify_image(img):
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(np.random.uniform(0.7, 1.3))  # Randomly enhance color
    img = img.rotate(np.random.uniform(-10, 10))  # Rotate slightly
    return img

# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')  # Show homepage first

@app.route('/index')
def index():
    return render_template('index.html')  # Redirected page

# Function to get survival advice
def get_survival_advice(description):
    prompt = f"Provide survival advice for a person stranded in the wilderness who encounters a {description}. Include whether it is safe, edible, or useful for survival."
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Adjust this to the correct model if needed
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

# Route to handle image upload and prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        description, confidence, img = predict_and_get_details(file_path)
        
        # Initialize img_path_modified
        img_path_modified = file_path

        attempts = 0
        while confidence < 0.5 and attempts < 3:  # Limit to 3 attempts for image modification
            img = modify_image(img)
            attempts += 1
            img_path_modified = os.path.join(app.config['UPLOAD_FOLDER'], f"modified_{filename}")
            img.save(img_path_modified)  # Save the modified image
            description, confidence, img = predict_and_get_details(img_path_modified)

        # Get actual survival advice from Groq API
        survival_advice = get_survival_advice(description)

        # Convert confidence to standard float
        confidence = float(confidence)  

        return jsonify({
            'description': description,
            'confidence': confidence,
            'survival_advice': survival_advice,  # Now generated by Groq
            'image_path': img_path_modified
        })

if __name__ == '__main__':
    app.run(debug=True)