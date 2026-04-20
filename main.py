from flask import Flask, request, jsonify, send_from_directory
from detector import classify_waste, classify_text
import base64, numpy as np, cv2

app = Flask(__name__, static_folder="../frontend", static_url_path="")


# 🌐 HOME PAGE
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# 🔤 TEXT DETECTION
@app.route('/detect_text', methods=['POST'])
def detect_text():
    return jsonify(classify_text(request.json['text']))


# 📁 IMAGE UPLOAD (FIXED)
@app.route('/classify', methods=['POST'])
def classify():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file received"})

        file = request.files['image']

        if file.filename == '':
            return jsonify({"error": "No file selected"})

        import numpy as np
        import cv2

        # convert image
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # 🔥 PASS filename separately (IMPORTANT FIX)
        result = classify_waste(img, file.filename)

        return jsonify(result)

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"error": "Upload failed"})

# 📷 CAMERA DETECTION
@app.route('/detect_live', methods=['POST'])
def detect_live():
    data = request.json['image']
    img_data = data.split(',')[1]

    img_bytes = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return jsonify(classify_waste(img))


# ▶️ RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)