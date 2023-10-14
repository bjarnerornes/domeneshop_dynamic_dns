# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Run app.py when the container launches
CMD ["python", "run.py"]
