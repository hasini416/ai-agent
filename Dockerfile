# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install all dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your project files
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
