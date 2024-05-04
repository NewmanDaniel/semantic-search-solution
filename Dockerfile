# Use an official Python runtime as the base image
#FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    virtualenv \
    ffmpeg \
    rabbitmq-server \
    redis-server


# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY ss_back_end /app

# Run sample training session. This enables it to download all needed model / tensor files so it is included in the image.
RUN echo "Running a test training step, which will download necessary model files so they are cached in the image"
RUN python3 -m ss_app.semantic_search sample_data/financial_compliance_feedback_database.csv

#CMD ["asdfpython3", "-m", "ss_app.semantic_search", "sample_data", "financial_compliance_feedback_database.csv"]
#CMD ["asdfijasdoifjaosidjfoiasdjf", "-m", "ss_app.semantic_search", "sample_data", "financial_compliance_feedback_database.csv"]

# Expose the port on which your Django application will run (change if necessary)
EXPOSE 8000

# Start RabbitMQ and Redis services when the container starts
#CMD ["rabbitmq-server", "&", "redis-server"]


# Run the Django development server
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["/bin/bash"]
