from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from io import BytesIO
import docx

app = FastAPI()

class FileURL(BaseModel):
    url: str

@app.post("/extract-text")
async def extract_text_from_docx(file: FileURL):
    try:
        # Télécharger le fichier .docx depuis l'URL
        response = requests.get(file.url)
        response.raise_for_status()

        # Charger le fichier dans python-docx
        doc = docx.Document(BytesIO(response.content))

        # Extraire le texte
        full_text = "\n".join([para.text for para in doc.paragraphs])

        return {"text": full_text}

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=400, content={"error": f"Erreur lors du téléchargement du fichier : {str(e)}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Erreur lors du traitement du fichier : {str(e)}"})
