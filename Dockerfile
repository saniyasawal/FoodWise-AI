FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend application and trained model
COPY backend/ ./backend/
COPY models/ ./models/

# Cloud Run listens on port 8080
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
