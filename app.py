from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
from io import BytesIO
import docx

app = FastAPI()

# === Endpoint de ping pour cron-job.org ===
@app.get("/ping")
def ping():
    return {"status": "ok"}

# === Modèle pour recevoir une URL ===
class FileURL(BaseModel):
    url: str

# === Taille maximale autorisée (8 Mo) ===
MAX_FILE_SIZE_MB = 8
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

@app.post("/extract-text")
async def extract_text_from_docx(file: FileURL):
    try:
        response = requests.get(file.url, stream=True)
        response.raise_for_status()

        # Vérification de la taille du fichier AVANT téléchargement complet
        file_size = int(response.headers.get('Content-Length', 0))
        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"Le fichier est trop volumineux ({file_size / 1024 / 1024:.2f} Mo). Limite autorisée : {MAX_FILE_SIZE_MB} Mo."
            )

        # Lecture et extraction du texte
        doc = docx.Document(BytesIO(response.content))
        full_text = "\n".join([para.text for para in doc.paragraphs])

        return {"text": full_text}

    except requests.exceptions.RequestException as e:
        return JSONResponse(status_code=400, content={"error": f"Erreur lors du téléchargement du fichier : {str(e)}"})

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"error": e.detail})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Erreur lors du traitement du fichier : {str(e)}"})
