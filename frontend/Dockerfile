
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the Streamlit port
EXPOSE 5002

# Start the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=5002"]
