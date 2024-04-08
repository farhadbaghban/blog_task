# Use the official Python base image
FROM python

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -U pip && pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /app/

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8080","--reload"]