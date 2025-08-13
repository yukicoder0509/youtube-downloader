FROM python:3.12-slim

# Copy uv binary from official image for efficiency
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

# Set environment variables for uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copy lock file and project metadata first to leverage Docker caching
COPY uv.lock pyproject.toml /app/

# Install dependencies using uv sync --frozen
# Use a cache mount for faster rebuilds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY /app /app

CMD ["bash"]