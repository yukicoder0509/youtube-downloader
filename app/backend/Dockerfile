FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for building some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*


# Install uv (the virtual environment manager)
RUN pip install --upgrade pip \
    && pip install uv

# Copy project files
COPY ./pyproject.toml ./uv.lock* ./

# Create virtual environment using uv
RUN uv sync

# Copy remaining backend source code
COPY ./backend ./backend

# Expose the port that FastAPI will listen on
EXPOSE 8000

# Start FastAPI using uvicorn with multiple workers
# Note: activate the uv environment before running
ENV MEDIA_DOWNLOAD_DIR=/media
CMD ["bash", "-c", "source ./.venv/bin/activate && uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4"]