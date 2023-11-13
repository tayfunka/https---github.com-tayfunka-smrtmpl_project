FROM python:3.11

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Run your application when the container launches
CMD ["python3", "run.py"]