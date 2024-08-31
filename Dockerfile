FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy all application files to the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.webhook.webhook_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]
