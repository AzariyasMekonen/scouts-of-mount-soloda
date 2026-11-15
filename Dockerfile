FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/src/

RUN mkdir -p /output && chmod 777 /output

ENV OUTPUT_DIR=/output \
    OUTPUT_FILENAME=recon_dispatch.txt

ENTRYPOINT ["python3", "/app/src/generate.py"]
