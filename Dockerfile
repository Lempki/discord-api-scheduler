FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir build && python -m build --wheel

FROM python:3.12-slim AS runtime
RUN useradd --create-home appuser
WORKDIR /app
COPY --from=builder /build/dist/*.whl .
RUN pip install --no-cache-dir *.whl && rm *.whl
RUN mkdir -p /data && chown appuser /data
USER appuser
EXPOSE 8000
CMD ["uvicorn", "scheduler_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
