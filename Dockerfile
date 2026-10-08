FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

COPY prompts ./prompts
COPY config ./config
COPY scripts ./scripts
COPY evals ./evals
COPY tests ./tests

COPY prompt_app.py .
COPY check_prompt_pin.py .
COPY logistics_mcp_versioned.py .
COPY clinics.json .

EXPOSE 8000

CMD ["uvicorn","prompt_app:app","--host","0.0.0.0","--port","8000"]