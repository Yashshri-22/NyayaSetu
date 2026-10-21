# NyayaSetu

**Bridging the Gap Between Law and Understanding**

NyayaSetu is an academic prototype for understanding legal documents with Generative AI and Retrieval-Augmented Generation (RAG). It is designed to help users explore uploaded documents, review clauses, ask questions, and view explanations supported by retrieved document context.

> **Important:** NyayaSetu is an informational prototype, not a substitute for a qualified lawyer. Explanations and risk flags may be incomplete or incorrect. Do not use the application as the sole basis for legal, financial, or contractual decisions.

---

## 1. Features

- Upload PDF and DOCX documents.
- Extract text from supported documents.
- Split document text into chunks and index it for retrieval.
- Ask questions about an uploaded document and review the retrieved context.
- Generate summaries and plain-language explanations.
- Flag potentially important clauses using preliminary heuristics.
- Explore basic what-if scenarios and draft-generation features, where implemented.
- Translate text through the configured Gemini API integration, where implemented.
- Register and log in using JWT-based authentication.
- Store application records in PostgreSQL and document embeddings in ChromaDB.
- Run the application with Docker Compose.

**Limitations**
- Scanned PDFs may require OCR. Install Tesseract OCR if the project’s OCR workflow is enabled.
- Risk flags are preliminary indicators, not legal conclusions.
- Answers depend on the quality and completeness of the uploaded document and retrieved context.
- Reliable legal-source retrieval requires verified legal materials to be ingested into the application.
- Sample agreements are fictional test documents and are not real contracts.

---

## 2. Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| Backend API | Python, FastAPI, Uvicorn |
| Database | PostgreSQL 16 |
| ORM / database access | SQLAlchemy, Psycopg |
| Vector store | ChromaDB |
| Language model | Google Gemini API |
| Authentication | JWT |
| Document parsing | PyMuPDF, python-docx |
| Deployment | Docker, Docker Compose |
| Testing | pytest, HTTPX |

---

## 3. Requirements

Install the following before starting:

1. **Docker Desktop** for Windows, with the Linux container engine enabled.
2. **WSL 2**, if required by your Docker Desktop installation.
3. **Git**, if you are cloning the project.
4. A valid **Gemini API key** if you want to use AI-powered features.

For running the application locally without Docker, also install:
- Python 3.11 or a Python version supported by the project dependencies.
- Node.js and npm.
- Tesseract OCR, if scanned-document OCR is required.

Check whether Docker is available in PowerShell:

```powershell
docker --version
docker compose version
docker info
```

`docker info` should display **Server** information. If it reports that it cannot connect to the Docker daemon or Linux engine, start or repair Docker Desktop before continuing.

---

## 4. Open the Project Folder

Open PowerShell and move to the project directory. Example:

```powershell
cd "$HOME\Downloads\NyayaSetu_Project\nyayasetu"
```

Use the directory that actually contains `compose.yaml` or `docker-compose.yml`. Confirm the files:

```powershell
Get-ChildItem
```

You should see the Compose file and folders such as `backend` and `frontend`.

> Run the commands in this README from the project root unless a step explicitly says otherwise.

---

## 5. Configure Environment Variables

Create a `.env` file in the project root if one does not already exist. If the repository provides `.env.example`, copy it first:

```powershell
Copy-Item .env.example .env
```

If `.env.example` does not exist, create `.env` manually and add the variables expected by your project configuration. The following is an example based on the current project setup:

```dotenv
GEMINI_API_KEY=replace_with_your_new_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
JWT_SECRET=replace_with_a_long_random_secret
DATABASE_URL=postgresql+psycopg://nyaya:nyaya@postgres:5432/nyayasetu
CHROMA_PERSIST_DIR=/app/chroma_data
UPLOAD_DIR=/app/uploads
MAX_UPLOAD_MB=20
FRONTEND_ORIGIN=http://localhost:5173
```

### Generate a JWT secret

Run this in PowerShell from a terminal where Python is available:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the generated value into `JWT_SECRET` in `.env`.

### API key and secret safety

- Replace the placeholder with your own valid Gemini API key.
- If an API key or secret has been shared publicly or committed to a repository, revoke or rotate it.
- Never commit `.env` to GitHub or share it in screenshots.
- Ensure `.env` is listed in `.gitignore`.
- Do not use example database credentials or development secrets in a production deployment.
- The `DATABASE_URL` above uses the Compose service name `postgres`; that is appropriate for containers on the Compose network. A locally running backend may need a different database hostname, such as `localhost`.

---

## 6. Build and Start the Application with Docker

Make sure Docker Desktop is running, then run these commands from the project root.

### First run, or after changing dependencies / Docker configuration

```powershell
docker compose up --build -d
```

This builds images when necessary and starts the services in the background.

### Start without rebuilding

```powershell
docker compose up -d
```

### Check service status

```powershell
docker compose ps
```

Wait until the required services are running and the database health check, if configured, reports healthy.

### Open the application

| Service | Local address |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| FastAPI Swagger documentation | http://localhost:8000/docs |
| PostgreSQL | `localhost:5432` (database client only) |

The browser URLs above assume the Compose file maps these ports to the host. If your Compose configuration uses different ports, use the mappings shown in that file.

---

## 7. Basic Usage

1. Start Docker Desktop.
2. Start the project using `docker compose up -d`.
3. Open the frontend at `http://localhost:5173`.
4. Register an account, or log in if an account already exists.
5. Upload a supported PDF or DOCX document.
6. Wait for extraction and indexing to complete.
7. Ask a question about the uploaded document or use the available summary, explanation, risk-flag, what-if, and drafting features.
8. Review the evidence or retrieved context shown with the answer.
9. Treat generated content as assistance for document review, not as professional legal advice.

If registration or another request fails, inspect the backend logs before changing frontend CORS settings.

---

## 8. Stop, Restart, and Rebuild

### Stop the services

```powershell
docker compose stop
```

This stops the running services but keeps the containers and data.

### Start services that were stopped

```powershell
docker compose start
```

### Restart all services

```powershell
docker compose restart
```

### Stop and remove containers and the Compose network

```powershell
docker compose down
```

This normally preserves named volumes, such as the database volume, so stored database data is retained.

### Rebuild and restart after code or dependency changes

```powershell
docker compose up --build -d
```

If you changed backend dependencies and need a clean backend image:

```powershell
docker compose build --no-cache backend
docker compose up -d --no-deps backend
```

Use `--no-cache` only when necessary; it can take longer and use more disk space.

> **Data warning:** Do not run `docker compose down -v` unless you intentionally want to remove Compose-managed volumes. Removing the database volume can permanently delete local application data.

---

## 9. View Logs and Diagnose Services

### View all service logs

```powershell
docker compose logs
```

### Follow logs live

```powershell
docker compose logs -f
```

### View only backend logs

```powershell
docker compose logs --tail=100 backend
```

Follow backend logs live:

```powershell
docker compose logs -f backend
```

### View frontend logs

```powershell
docker compose logs --tail=100 frontend
```

### View PostgreSQL logs

```powershell
docker compose logs --tail=100 postgres
```

Press `Ctrl+C` to stop following logs. This does not stop the containers.

### Check service status again

```powershell
docker compose ps
```

If only PostgreSQL appears, the backend and frontend may have stopped or failed to start. Review their logs and start the application again after resolving the error.

---

## 10. Troubleshooting

### A. Registration returns `500 Internal Server Error`

First inspect the backend traceback:

```powershell
docker compose logs --tail=150 backend
```

One known issue in this project setup is a possible incompatibility between Passlib and newer versions of `bcrypt`. The traceback may mention password hashing or bcrypt backend initialization.

Check the dependency declarations in `backend/requirements.txt`. If the project still uses an unpinned `passlib[bcrypt]>=1.7` dependency, try pinning compatible versions:

```text
passlib==1.7.4
bcrypt==4.0.1
```

Replace the old Passlib dependency line with the two lines above, save the file, and verify the saved contents:

```powershell
Select-String -Path .\backend\requirements.txt -Pattern "passlib|bcrypt"
```

Then rebuild and recreate the backend:

```powershell
docker compose build --no-cache backend
docker compose up -d --no-deps backend
```

If the container starts successfully, verify the installed versions:

```powershell
docker compose exec backend python -c "import bcrypt, passlib; print('bcrypt:', bcrypt.__version__); print('passlib:', passlib.__version__)"
```

If the build or container still fails, use the newest traceback in the backend logs. Do not assume this dependency change resolves every possible registration error.

**Important:** Installing packages in a local Python virtual environment does not change the packages inside the Docker container. Rebuild the backend image when the container uses the updated requirements file.

### B. Browser reports a CORS error

A browser CORS message can occur when the backend is down or returns an error, so check service status first:

```powershell
docker compose ps
docker compose logs --tail=100 backend
```

Open the API documentation directly:

`http://localhost:8000/docs`

If the backend is not responding, fix the backend error before editing CORS settings. Confirm that the frontend origin configured in `.env` matches the actual frontend address, normally:

```dotenv
FRONTEND_ORIGIN=http://localhost:5173
```

After changing environment variables, recreate the relevant service:

```powershell
docker compose up -d --force-recreate backend
```

Only adjust the CORS middleware if the logs and configuration show that CORS itself is misconfigured. Avoid adding duplicate CORS middleware blindly.

### C. Docker reports `EOF`, cannot connect to the engine, or cannot open the Linux engine pipe

1. Save your work.
2. Open Docker Desktop and wait for it to finish starting.
3. In PowerShell, run:

```powershell
docker info
docker context ls
wsl --list --verbose
```

If Docker Desktop is stuck, close it and run:

```powershell
wsl --shutdown
```

Then reopen Docker Desktop, wait for the engine to start, and retry:

```powershell
docker info
docker compose ps
```

If the server section of `docker info` is still unavailable, the issue is with the Docker engine rather than the application code. Do not delete WSL distributions or reset Docker to factory defaults as an initial troubleshooting step.

### D. Docker reports insufficient disk space

Check free space on the drive used by Docker Desktop. You can remove unused build cache:

```powershell
docker builder prune
```

Review the confirmation prompt before proceeding. This removes unused build cache, not your source-code files. Other Docker cleanup commands may remove images or containers you still need.

Avoid deleting database volumes unless you have a backup and intentionally want to erase the local database.

### E. A service does not appear in `docker compose ps`

Run:

```powershell
docker compose ps -a
docker compose logs --tail=150 backend
docker compose logs --tail=150 frontend
```

Look for build errors, missing environment variables, dependency failures, port conflicts, or application exceptions. Resolve the specific error and then run:

```powershell
docker compose up --build -d
```

### F. Port already in use

If a port is already occupied, Docker may fail to bind it. Check the Compose port mappings and close the other application using that port, or update the host-side port mapping in the Compose file. If you change a port, use the new address when opening the app and update the frontend/API configuration if required.

---

## 11. Run the Backend Locally (Optional)

Use this only if you want to run the backend outside Docker and have configured a reachable PostgreSQL instance and any other required services.

Open a separate PowerShell terminal in the project root:

```powershell
cd .\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you may use the appropriate execution-policy option permitted on your computer, or run the virtual environment's Python executable directly.

Set the environment variables required by the backend. Remember that a local backend usually cannot resolve the Compose hostname `postgres`; update `DATABASE_URL` for your local database connection.

Start the backend using the command appropriate for the project. For a standard FastAPI application whose ASGI object is `app` in `app.main`:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If the module or application object differs in your project, use the actual entry point. The backend should then be available at `http://localhost:8000`, with documentation at `http://localhost:8000/docs`.

---

## 12. Run the Frontend Locally (Optional)

Open another PowerShell terminal:

```powershell
cd "$HOME\Downloads\NyayaSetu_Project\nyayasetu\frontend"
npm install
npm run dev
```

Vite commonly serves the frontend at `http://localhost:5173`. Use the URL printed in the terminal if it differs.

Make sure the frontend API base URL points to the backend address you are actually using. Do not run the local frontend and Docker frontend on the same host port at the same time unless you have changed the port mapping.

---

## 13. Tests and Evaluation

If the backend includes pytest tests, run them from the backend environment:

```powershell
cd .\backend
python -m pytest
```

If running inside Docker and the service is already running:

```powershell
docker compose exec backend python -m pytest
```

Test availability depends on the test files included in the project. Passing starter tests does not prove that all AI answers are correct or that the application is production-ready.

Suggested manual checks:
- Register and log in.
- Upload a small text-based PDF.
- Upload a DOCX file.
- Confirm extraction and indexing complete.
- Ask a question whose answer is explicitly present in the document.
- Check that the response includes relevant supporting context, if evidence display is implemented.
- Try a question whose answer is not present and confirm the app handles missing information appropriately.
- Test invalid file types and files larger than the configured upload limit.
- Review backend logs after each failure.

---

## 14. Project Structure

The exact structure may vary by version. A typical layout is:

```text
nyayasetu/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
├── compose.yaml / docker-compose.yml
├── .env
├── .env.example
└── README.md
```

Do not commit generated files, uploaded private documents, local databases, secrets, or environment files unless the repository explicitly requires them and they have been reviewed for sensitive content.

---

## 15. Privacy and Security

- Upload only documents you are permitted to process.
- Avoid uploading confidential legal, personal, or financial documents to a prototype unless you understand where the data is stored and which external services receive content.
- AI features may send document text or retrieved excerpts to the configured Gemini API. Review the provider's current data-handling terms before using sensitive data.
- Keep API keys, JWT secrets, database credentials, and uploaded files private.
- Use strong, unique secrets outside local development.
- Configure authentication, authorization, upload validation, logging, retention, and access controls before any public deployment.
- Do not expose PostgreSQL or the backend directly to the public internet without appropriate security controls.

---

## 16. Quick Command Reference

Run these from the project root:

| Task | Command |
|---|---|
| Build and start | `docker compose up --build -d` |
| Start existing containers | `docker compose start` |
| Stop services | `docker compose stop` |
| Restart services | `docker compose restart` |
| Stop and remove containers/network | `docker compose down` |
| Check status | `docker compose ps` |
| Follow all logs | `docker compose logs -f` |
| Show backend logs | `docker compose logs --tail=100 backend` |
| Rebuild backend without cache | `docker compose build --no-cache backend` |
| Recreate backend | `docker compose up -d --no-deps backend` |

---

## 17. Disclaimer

NyayaSetu is an academic demonstration of document processing and AI-assisted information retrieval. It does not provide legal representation or guaranteed legal interpretations. Always verify important information against the original document and consult a qualified legal professional for decisions that require legal advice.
