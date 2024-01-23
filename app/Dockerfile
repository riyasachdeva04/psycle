FROM python:3.11-slim

WORKDIR /main_app

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=main_app.py

# Expose the port used in the CMD (6000 in this case)
EXPOSE 6000

# Run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
