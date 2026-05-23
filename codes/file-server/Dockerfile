FROM python:3.13-alpine

RUN pip install flask --no-cache-dir

# Create non-root user
RUN adduser -D -h /app appuser

WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser app/ /app/app/
COPY --chown=appuser:appuser static/ /app/static/
COPY --chown=appuser:appuser main.py /app/

USER appuser

EXPOSE 7890

ENV FILESERVER_DIR=/data/downloads \
    FILESERVER_HOST=0.0.0.0 \
    FILESERVER_PORT=7890 \
    FILESERVER_PAGE_SIZE=15

CMD ["python3", "main.py"]
