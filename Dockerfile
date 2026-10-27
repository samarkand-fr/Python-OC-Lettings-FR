# Base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files for production (using temporary build key)
RUN SECRET_KEY="temporary-build-key-for-collectstatic" python manage.py collectstatic --noinput

# Expose default application port
EXPOSE 8000

# Run migrations and start production Gunicorn server
CMD ["sh", "-c", "python manage.py migrate && gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
