# Distributed C++ Processing Pipeline

This folder contains a distributed wrapper around your C++ image processing pipeline.

## Services

1. `input_service.py` — accepts `.ppm` uploads and forwards them to the processor service.
2. `processor_service.py` — saves upload locally, runs the C++ binary, and forwards the resulting `.pgm` file to the output service.
3. `output_service.py` — stores the final processed file and serves it for download.

## Architecture

- `input_service` receives `input.ppm` from the user.
- `processor_service` executes the C++ binary built from your `src/` code.
- `output_service` stores the final `output.pgm` and exposes download.
- All communication happens over HTTP.

## Installation

1. Open a terminal in `distributed_services`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Build the C++ processor binary from the project root:

```bash
cd ..
make processor
```

This produces `processor.exe` in the repository root.

## Run Services

Start each service in a separate terminal:

### Input Service

```bash
cd distributed_services
py -m uvicorn input_service:app --host 127.0.0.1 --port 8100
```

### Processor Service

```bash
cd distributed_services
py -m uvicorn processor_service:app --host 127.0.0.1 --port 8200
```

### Output Service

```bash
cd distributed_services
py -m uvicorn output_service:app --host 127.0.0.1 --port 8300
```

## How to Use

### Upload .ppm file

```bash
cd distributed_services
curl.exe -F "file=@../input.ppm" http://127.0.0.1:8100/upload
```

### Download processed file

```bash
curl.exe "http://127.0.0.1:8300/download?filename=input_output.pgm" -o output.pgm
```

### Download as PNG

```bash
curl.exe "http://127.0.0.1:8300/download?filename=input_output.pgm&format=png" -o output.png
```

### Check service status

```bash
curl.exe http://127.0.0.1:8100/status
curl.exe http://127.0.0.1:8200/status
curl.exe http://127.0.0.1:8300/status
```

## Frontend

A simple browser frontend is available at `distributed_services/frontend.html`.
Open it in a browser or serve it with a local HTTP server:

```bash
cd distributed_services
py -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080/frontend.html
```

## Docker support

A root-level `Dockerfile` and `docker-compose.yml` have been added for a stronger, containerized setup.

### Build and run all services with Docker Compose

```bash
cd C-Hardware-Accelerator-Model
docker compose up --build
```

This starts:
- Input Service on `http://127.0.0.1:8100`
- Processor Service on `http://127.0.0.1:8200`
- Output Service on `http://127.0.0.1:8300`

### Run just one service container

```bash
docker compose up input
```

## Deployment roadmap

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "distributed system with backend services and Docker"
git remote add origin <your-github-url>
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com.
2. Create a new web service.
3. Connect your GitHub repo.
4. Use the `distributed_services` folder or the root repository.
5. Set the start command for each service:

- `uvicorn input_service:app --host 0.0.0.0 --port 8100`
- `uvicorn processor_service:app --host 0.0.0.0 --port 8200`
- `uvicorn output_service:app --host 0.0.0.0 --port 8300`

### Step 3: Use one frontend

Use `frontend.html` as your single UI layer. It uploads the file to Input Service and provides output links from Output Service.

## Why this is strong

- Backend services remain separate and scalable.
- Frontend stays single and easy to use.
- GitHub stores code and Render deploys services.
- Docker makes the whole system reproducible and ready for real deployment.

## Notes

- The C++ processor binary executes your existing `src/` code.
- The final output is a grayscale `.pgm` file produced by the edge pipeline.
- You can download PNG output directly from the output service.
