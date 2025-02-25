# Use Python base image
FROM python:3.9-slim

# Set /app as the working directory inside the container
WORKDIR /app

# Copy in the dependencies list
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /app

# Expose port 3000 (used by Uvicorn)
EXPOSE 3000

# Default command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]