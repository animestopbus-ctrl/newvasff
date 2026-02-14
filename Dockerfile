FROM python:3.14-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Make the startup script executable
RUN chmod +x start.sh

# Start the application
CMD ["./start.sh"]
