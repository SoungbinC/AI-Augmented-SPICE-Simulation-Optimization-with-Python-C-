FROM python:3.10-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install pybind11 (from source to get CMake support)
RUN git clone https://github.com/pybind/pybind11.git /opt/pybind11 && \
    cd /opt/pybind11 && mkdir build && cd build && cmake .. && make install


# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
WORKDIR /app
COPY . .

# Build the cpp_blocks shared library
WORKDIR /app/cpp_blocks
RUN mkdir build && cd build && cmake .. && make


# Move shared object to app dir
WORKDIR /app
RUN cp cpp_blocks/build/*.so app/cpp_blocks.so

# Set working directory
WORKDIR /app/app

# Set PYTHONPATH to include the root /app directory
ENV PYTHONPATH=/app

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
