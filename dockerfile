# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /elyamash-backend

# Copy the current directory contents into the container at /app
COPY . /elyamash-backend

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]