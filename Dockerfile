FROM python:3.12

# Set the working directory in the container
WORKDIR /vm-application

# Copy the requirements file into the container at /vm-application
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container at /vm-application
COPY application.py .

CMD ["python", "./application.py"]
