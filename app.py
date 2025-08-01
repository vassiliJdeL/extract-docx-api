from flask import Flask, request, jsonify
import requests
from docx import Document
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
    return "API opérationnelle"

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json()
    docx_url = data.get("url")
    
    if not docx_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(docx_url)
        response.raise_for_status()

        file_stream = BytesIO(response.content)
        doc = Document(file_stream)
        text = "\n".join([p.text for p in doc.paragraphs])

        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
