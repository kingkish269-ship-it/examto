# INSECURE Dockerfile for study. Flagged by validator/dockerfile_lint.py.
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
RUN curl https://example.com/install.sh | sh
COPY . /app
CMD ["/app/run"]
# No non-root USER -> runs as root.
