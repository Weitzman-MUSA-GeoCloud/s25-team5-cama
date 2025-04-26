# Use the official lightweight Python 3.12 image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from your project into the container
COPY . .

# Install all dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Cloud Run (port must be 8080)
ENV PORT 8080

# Start the HTTP server using Functions Framework
# --target specifies the function name (your entry point)
# --port specifies the listening port
CMD ["functions-framework", "--target=query_map_property_info", "--port=8080"]
