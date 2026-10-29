# SECURE Dockerfile. Paired fix for ../insecure/Dockerfile.
FROM python:3.11-slim@sha256:deadbeefcafe
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 1000
HEALTHCHECK CMD ["python", "-c", "import sys; sys.exit(0)"]
CMD ["python", "app.py"]
