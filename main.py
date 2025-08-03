from flask import Flask, request, jsonify
from docx import Document
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return "API is running"

@app.route("/extract", methods=["POST"])
def extract_text():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        doc = Document(BytesIO(file.read()))
        text = "\n".join([para.text for para in doc.paragraphs])
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500