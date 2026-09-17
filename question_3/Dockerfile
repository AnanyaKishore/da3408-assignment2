FROM python:3.10-slim
WORKDIR /data
COPY shards/ .
WORKDIR /app
COPY validate.py .
CMD ["python", "validate.py"]