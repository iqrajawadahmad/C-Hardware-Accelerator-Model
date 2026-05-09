from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI(title="Input Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROCESSOR_URL = os.getenv("PROCESSOR_URL", "http://127.0.0.1:8200")
INPUT_DIR = os.path.join(os.path.dirname(__file__), "input_storage")

os.makedirs(INPUT_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    print("REQUEST RECEIVED")

    filename = file.filename
    print(" FILE NAME:", filename)

    if not filename.lower().endswith(".ppm"):
        print(" INVALID FILE TYPE")
        raise HTTPException(status_code=400, detail="Only .ppm files are supported")

    target_path = os.path.join(INPUT_DIR, filename)

    # save file
    with open(target_path, "wb") as f:
        f.write(await file.read())

    print(" FILE SAVED:", target_path)
    print(" FORWARDING TO PROCESSOR")

    # send to processor
    with open(target_path, "rb") as payload:
        files = {"file": (filename, payload, "image/x-portable-pixmap")}

        try:
            print(" CALLING PROCESSOR SERVICE...")
            resp = requests.post(f"{PROCESSOR_URL}/process", files=files, timeout=60)
            resp.raise_for_status()
            print("✅ PROCESSOR RESPONSE RECEIVED")

        except requests.RequestException as exc:
            print("PROCESSOR ERROR:", str(exc))
            raise HTTPException(status_code=500, detail=str(exc))

    return resp.json()


# HEALTH CHECK
@app.get("/health")
def health():
    print("HEALTH CHECK CALLED")
    return {"status": "ok"}


# STATUS
@app.get("/status")
def status():
    print("STATUS CHECK")
    return {
        "service": "input",
        "stored_files": os.listdir(INPUT_DIR)
    }