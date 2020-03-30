# We always start from an existing container
FROM python:3.8-slim-buster
# Copy dependency lists into container
COPY requirements.txt .
COPY requirements-dev.txt .
# Install dependencies
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
# Copy our code into the container
COPY app.py .
# Copy the HTML page templates directory
COPY templates templates
# Copy the version number into the container
COPY VERSION.txt .
# Our code runs on port 5000, so allow access
EXPOSE 5000
# Set the FLASK_APP environment variable
ENV FLASK_APP app.py
# This is the command that is executed when the container starts
# Note we've added --host=0.0.0.0 as by default only local users would
# be able to access the application.
CMD [ "flask", "run", "--host=0.0.0.0" ]
