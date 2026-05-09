    # from fastapi import FastAPI, UploadFile, File, HTTPException
    # from fastapi.middleware.cors import CORSMiddleware
    # import os
    # import requests
    # import subprocess

    # app = FastAPI(title="Processor Service")
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    # OUTPUT_URL = os.getenv("OUTPUT_URL", "http://127.0.0.1:8300")
    # STORAGE_DIR = os.path.join(os.path.dirname(__file__), "processor_storage")

    # default_processor = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "processor"))
    # default_processor_exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "processor.exe"))
    # PROCESSOR_EXE = os.getenv("PROCESSOR_EXE", default_processor)
    # if not os.path.exists(PROCESSOR_EXE) and os.path.exists(default_processor_exe):
    #     PROCESSOR_EXE = default_processor_exe

    # os.makedirs(STORAGE_DIR, exist_ok=True)

    # @app.post("/process")
    # def process_file(file: UploadFile = File(...)):
    #     if not file.filename.lower().endswith(".ppm"):
    #         raise HTTPException(status_code=400, detail="Only .ppm files are supported")

    #     input_path = os.path.join(STORAGE_DIR, file.filename)
    #     output_name = os.path.splitext(file.filename)[0] + "_output.pgm"
    #     output_path = os.path.join(STORAGE_DIR, output_name)

    #     with open(input_path, "wb") as f:
    #         f.write(file.file.read())

    #     if not os.path.exists(PROCESSOR_EXE):
    #         raise HTTPException(status_code=500, detail=f"Processor binary not found: {PROCESSOR_EXE}")

    #     try:
    #         completed = subprocess.run([PROCESSOR_EXE, input_path, output_path], check=True, capture_output=True, text=True)
    #     except subprocess.CalledProcessError as exc:
    #         raise HTTPException(status_code=500, detail=f"Processor failed: {exc.stderr or exc.stdout}")

    #     with open(output_path, "rb") as payload:
    #         files = {"file": (output_name, payload, "image/x-portable-graymap")}
    #         try:
    #             resp = requests.post(f"{OUTPUT_URL}/store", files=files, timeout=60)
    #             resp.raise_for_status()
    #         except requests.RequestException as exc:
    #             raise HTTPException(status_code=500, detail=f"Output service error: {exc}")

    #     return {"status": "processed", "output_file": output_name, "output_service": f"{OUTPUT_URL}/download?filename={output_name}"}

    # @app.get("/status")
    # def status():
    #     return {"service": "processor", "stored_files": os.listdir(STORAGE_DIR), "processor_exe": PROCESSOR_EXE}
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import subprocess

app = FastAPI(title="Processor Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_URL = os.getenv("OUTPUT_URL", "http://output:8300")
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "processor_storage")


default_processor = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "processor"))
#default_processor_exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "processor.exe"))

PROCESSOR_EXE = os.getenv("PROCESSOR_EXE", default_processor)

##if not os.path.exists(PROCESSOR_EXE) and os.path.exists(default_processor_exe):
    #PROCESSOR_EXE = default_processor_exe

os.makedirs(STORAGE_DIR, exist_ok=True)


@app.post("/process")
def process_file(file: UploadFile = File(...)):

    print(" PROCESSOR SERVICE TRIGGERED")

    # validate file
    if not file.filename.lower().endswith(".ppm"):
        print(" INVALID FILE TYPE")
        raise HTTPException(status_code=400, detail="Only .ppm files are supported")

    print("FILE RECEIVED:", file.filename)

    input_path = os.path.join(STORAGE_DIR, file.filename)
    output_name = os.path.splitext(file.filename)[0] + "_output.pgm"
    output_path = os.path.join(STORAGE_DIR, output_name)

    # save input
    with open(input_path, "wb") as f:
        f.write(file.file.read())

    print(" INPUT SAVED:", input_path)
    print(" STARTING PROCESSING PIPELINE...")

    # check processor binary
    if not os.path.exists(PROCESSOR_EXE):
        print(" PROCESSOR BINARY NOT FOUND")
        raise HTTPException(status_code=500, detail=f"Processor binary not found: {PROCESSOR_EXE}")

    # run processor
    try:
        print(" RUNNING HARDWARE ACCELERATOR...")
        subprocess.run([PROCESSOR_EXE, input_path, output_path], check=True)
        print(" PROCESSING COMPLETE")

    except Exception as exc:
        print(" PROCESSING FAILED:", exc)
        raise HTTPException(status_code=500, detail=f"Processor failed: {exc}")

    # send to output service
    try:
        print("SENDING TO OUTPUT SERVICE...")
        with open(output_path, "rb") as payload:
            files = {"file": (output_name, payload, "image/x-portable-graymap")}

            resp = requests.post(
                f"{OUTPUT_URL.rstrip('/')}/store",
                files=files,
                timeout=60
            )

        print("RESPONSE CODE:", resp.status_code)
        print(" RESPONSE TEXT:", resp.text)
        resp.raise_for_status()

        print("SENT TO OUTPUT SUCCESSFULLY")

    except requests.RequestException as exc:
        print(" OUTPUT SERVICE ERROR:", exc)
        raise HTTPException(status_code=500, detail=f"Output service error: {exc}")

    return {
        "status": "processed",
        "output_file": output_name,
        "output_service": f"{OUTPUT_URL.rstrip('/')}/download?filename={output_name}"
    }


# HEALTH CHECK
@app.get("/health")
def health():
    print(" HEALTH CHECK CALLED (PROCESSOR)")
    return {"status": "ok"}


# STATUS
@app.get("/status")
def status():
    print(" STATUS CHECK (PROCESSOR)")
    return {
        "service": "processor",
        "stored_files": os.listdir(STORAGE_DIR),
        "processor_exe": PROCESSOR_EXE
    }