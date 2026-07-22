FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so this layer caches across code-only changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# EDI talks to Ollama over HTTP; point OLLAMA_HOST at your host machine's
# Ollama install (default below assumes Docker Desktop's host.docker.internal).
# If Ollama is unreachable, the app falls back to its built-in offline
# responses rather than failing — see ollama_client.py.
ENV OLLAMA_HOST=http://host.docker.internal:11434

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "Nextstreet-Interview-Demo.py"]
