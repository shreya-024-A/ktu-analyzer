# Use Python image
FROM python:3.12-slim

# Install Tesseract OCR software
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Set working directory
WORKDIR /app

# Install Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Run migrations and start the server
CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ktu_project.wsgi:application --bind 0.0.0.0:$PORT"