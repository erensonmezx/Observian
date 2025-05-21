# Dockerfile

FROM python:3.9-slim

# Set workdir to /app
WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd
# Copy everything into /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Python can find the app module
ENV PYTHONPATH=/app

# Run FastAPI app
COPY start.sh .
RUN chmod +x ./start.sh
CMD ["./start.sh"]