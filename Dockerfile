# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

FROM base AS builder

# Enable bytecode compilation and copy from the cache instead of linking since it's a mounted volume
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Install the project into `/app`
WORKDIR /app

# Installing curl, build-essential and rust
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential && \
    curl --proto '=https' --tlsv1.3 https://sh.rustup.rs -sSf | sh -s -- -y && \
    apt-get remove --purge -y curl && \
    apt-get autoremove -y

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Add python virtual environment and cargo to PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV PATH="/root/.cargo/bin:${PATH}"

# Building the native Rust extension
RUN maturin develop -r --uv -m /app/audio-lib/Cargo.toml


FROM base AS final

# Copy the application files into the final image
COPY --from=builder /app /app

# Add python virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Project launch
CMD ["uv", "run", "-m", "bot.main.py"]