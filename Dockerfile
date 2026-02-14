FROM python:3.14-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Start the application directly using Gunicorn and Render's dynamic port
CMD gunicorn bot:app --bind 0.0.0.0:$PORT
