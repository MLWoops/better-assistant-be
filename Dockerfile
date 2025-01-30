FROM python:3.11-slim-bookworm as builder

# Set the working directory
WORKDIR /app

# Install necessary tools
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN pip3 install uv --no-cache-dir

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock ./

# Install dependencies in a virtual environment
RUN python3 -m uv sync


# Runtime image
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Set environment variables for Python
ENV PATH="/app/.venv/bin:$PATH"

# Copy project files
COPY . .

# Entrypoint
ENTRYPOINT ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]