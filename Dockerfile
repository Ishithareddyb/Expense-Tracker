FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY app/ /app
COPY templates/ /app/templates
COPY static/ /app/static

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Flask app
ENV FLASK_APP=main.py
CMD ["flask", "run", "--host=0.0.0.0"]
