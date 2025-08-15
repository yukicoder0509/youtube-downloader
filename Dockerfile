# Stage 1 – frontend build
FROM node:23-alpine AS frontend-builder

WORKDIR /app/frontend

# Install dependencies
COPY app/frontend/package*.json ./
RUN npm ci

# Copy source files and build
COPY app/frontend/ ./
ENV VITE_BUILD_MODE=production
RUN npx vite build --mode=${VITE_BUILD_MODE}

# Stage 2 – backend build
FROM python:3.12-slim AS backend

WORKDIR /app

# Install system dependencies and uv
COPY ytdlp-dependencies.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
    $(cat ytdlp-dependencies.txt) \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install uv

# Copy project files and install dependencies
COPY app/backend/pyproject.toml app/backend/uv.lock* ./
RUN uv sync

# Copy backend source code
COPY app/backend/backend ./backend

# Copy frontend build into backend
COPY --from=frontend-builder /app/frontend/dist ./backend/frontend-dist

# Final stage
FROM backend

WORKDIR /app/backend
EXPOSE 8000
ENV MEDIA_DOWNLOAD_DIR=/media
CMD ["bash","-c","source ../.venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"]