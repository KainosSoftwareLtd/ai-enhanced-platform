# Stage 1: Builder for Python 3.9
FROM python:3.9 AS builder39

WORKDIR /app

# Copy the requirements file for Python 3.9
COPY requirements.txt requirements.txt

# Install dependencies for Python 3.9
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY . /app

# Stage 2: Builder for Python 3.12
FROM python:3.12 AS builder312

WORKDIR /app

# Copy the requirements file for Python 3.12
COPY requirements.txt requirements.txt

# Install dependencies for Python 3.12
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY . /app

# Stage 3: Create the final image using Distroless for a minimal and secure environment
FROM gcr.io/distroless/python3-debian11

# Set the working directory in the Distroless image
WORKDIR /app

# Copy the installed Python 3.9 dependencies from the builder39 stage
COPY --from=builder39 /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder39 /usr/local/bin /usr/local/bin

# Copy the installed Python 3.12 dependencies from the builder312 stage
COPY --from=builder312 /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder312 /usr/local/bin /usr/local/bin

# Copy application code from the builder312 stage (assuming it's the same)
COPY --from=builder312 /app .

# Attempt to adjust PYTHONPATH for both versions
ENV PYTHONPATH=/usr/local/lib/python3.9/site-packages:/usr/local/lib/python3.12/site-packages

# Distroless images do not include a shell, so CMD should not use shell syntax
CMD ["/usr/local/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
