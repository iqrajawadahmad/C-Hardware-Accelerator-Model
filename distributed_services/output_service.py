# from fastapi import FastAPI, UploadFile, File, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse, StreamingResponse
# import os
# import io
# from PIL import Image

# app = FastAPI(title="Output Service")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# STORAGE_DIR = os.path.join(os.path.dirname(__file__), "output_storage")

# os.makedirs(STORAGE_DIR, exist_ok=True)

# @app.post("/store")
# def store_file(file: UploadFile = File(...)):
#     filename = file.filename
#     if not filename.lower().endswith(".pgm"):
#         raise HTTPException(status_code=400, detail="Only .pgm files are supported for output")

#     target_path = os.path.join(STORAGE_DIR, filename)
#     with open(target_path, "wb") as f:
#         f.write(file.file.read())

#     return {"status": "stored", "filename": filename}

# @app.get("/download")
# def download_file(filename: str, format: str = Query("pgm", pattern="^(pgm|png)$")):
#     file_path = os.path.join(STORAGE_DIR, filename)
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     if format == "pgm":
#         return FileResponse(file_path, media_type="image/x-portable-graymap", filename=filename)

#     # Convert PGM to PNG on the fly
#     try:
#         with Image.open(file_path) as img:
#             png_bytes = io.BytesIO()
#             img.save(png_bytes, format="PNG")
#             png_bytes.seek(0)
#     except Exception as exc:
#         raise HTTPException(status_code=500, detail=f"Conversion failed: {exc}")

#     png_name = os.path.splitext(filename)[0] + ".png"
#     return StreamingResponse(png_bytes, media_type="image/png", headers={"Content-Disposition": f"attachment; filename=\"{png_name}\""})

# @app.get("/status")
# def status():
#     return {"service": "output", "stored_files": os.listdir(STORAGE_DIR)}

import time
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
import os
import io
from PIL import Image
from supabase import create_client

app = FastAPI(title="Output Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "output_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)


# SUPABASE INIT
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.post("/store")
def store_file(file: UploadFile = File(...)):

    print(" STORE REQUEST RECEIVED")

    filename = file.filename
    print("FILE RECEIVED:", filename)

    if not filename.lower().endswith(".pgm"):
        print("INVALID FILE TYPE")
        raise HTTPException(status_code=400, detail="Only .pgm files are supported")

    file_bytes = file.file.read()

    # SAVE 
    target_path = os.path.join(STORAGE_DIR, filename)
    with open(target_path, "wb") as f:
        f.write(file_bytes)

    print("SAVED", target_path)

    # CONVERT + UPLOAD
    try:
        print("CONVERTING PGM → PNG...")

        png_bytes_io = io.BytesIO()
        with Image.open(io.BytesIO(file_bytes)) as img:
            img.save(png_bytes_io, format="PNG")

        png_bytes = png_bytes_io.getvalue()

        png_filename = os.path.splitext(filename)[0] + f"_{int(time.time())}.png"

        print("UPLOADING TO SUPABASE...")

        supabase.storage.from_("outputs").upload(
            path=png_filename,
            file=png_bytes,
            file_options={"content-type": "image/png", "upsert": "true"}
        )

        permanent_url = f"{SUPABASE_URL}/storage/v1/object/public/outputs/{png_filename}"

        print("UPLOAD SUCCESS")
        print(" URL:", permanent_url)

    except Exception as e:
        print(" SUPABASE ERROR:", e)
        permanent_url = None

    return {
        "status": "stored",
        "filename": filename,
        "permanent_url": permanent_url
    }


@app.get("/download")
def download_file(filename: str, format: str = Query("pgm", pattern="^(pgm|png)$")):

    print("⬇ DOWNLOAD REQUEST:", filename, format)

    file_path = os.path.join(STORAGE_DIR, filename)

    if not os.path.exists(file_path):
        print(" FILE NOT FOUND")
        raise HTTPException(status_code=404, detail="File not found")

    if format == "pgm":
        print(" RETURNING PGM")
        return FileResponse(file_path, media_type="image/x-portable-graymap", filename=filename)

    try:
        print("CONVERTING TO PNG...")
        with Image.open(file_path) as img:
            png_bytes = io.BytesIO()
            img.save(png_bytes, format="PNG")
            png_bytes.seek(0)

    except Exception as exc:
        print(" CONVERSION ERROR:", exc)
        raise HTTPException(status_code=500, detail=f"Conversion failed: {exc}")

    png_name = os.path.splitext(filename)[0] + ".png"

    print("SENDING PNG")

    return StreamingResponse(
        png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=\"{png_name}\""}
    )


# HEALTH CHECK
@app.get("/health")
def health():
    print("HEALTH CHECK CALLED (OUTPUT)")
    return {"status": "ok"}


# STATUS
@app.get("/status")
def status():
    print("STATUS CHECK (OUTPUT)")
    return {
        "service": "output",
        "stored_files": os.listdir(STORAGE_DIR)
    }