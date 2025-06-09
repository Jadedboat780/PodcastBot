# Отдельный "сборочный" образ
FROM python:3.13-slim AS base

FROM base AS builder
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Enable bytecode compilation and copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install the project into `/app`
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM base AS final
# Copy the application files into the final image
COPY --from=builder /app /app

# Add python virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Project launch
CMD ["python", "-m", "bot.main.py"]
