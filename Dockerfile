# Use a lightweight, standardized official Python base image
FROM python:3.11-slim

# Establish secure internal working directory paths
WORKDIR /app

# Install standard system requirements for core math compiling
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy frozen environment dependency arrays 
COPY requirements.txt .

# Install locked package libraries without caching local artifacts
RUN pip install --no-cache-dir -r requirements.txt

# Sync production files and schema catalogs into the active image
COPY core_pipeline/ ./core_pipeline/
COPY data_schemas/ ./data_schemas/
COPY virtual_cohort_engine.py .
COPY process_table_9.py .
COPY test_pipeline.py .

# Define default execution task to compile validation logs instantly
CMD ["sh", "-c", "python test_pipeline.py && python virtual_cohort_engine.py && python process_table_9.py"]
