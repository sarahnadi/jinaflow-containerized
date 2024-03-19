FROM jinaai/jina:latest-daemon

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Entrypoint script
CMD ["jina", "flow", "--uses", "flow.yml"]