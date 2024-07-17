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

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variable
<<<<<<< HEAD
ENV FLASK_APP main.py
=======
ENV FLASK_APP=main.py
>>>>>>> b70a26f0af4a25060ed6b7bdf18170b308615d2b

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
