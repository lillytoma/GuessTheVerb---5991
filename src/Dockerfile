# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask
RUN pip install python-dotenv
RUN pip install pymongo
RUN pip install levenshtein

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variable
ENV FLASK_APP=main.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
