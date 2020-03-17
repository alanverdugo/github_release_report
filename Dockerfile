FROM python:3.8-slim

# Install Python modules.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

# Create a directory to store the resultant files.
RUN mkdir /output

COPY report_releases.py /report_releases.py

# Execute the program.
ENTRYPOINT ["/report_releases.py"]
# Get arguments from the CLI.
CMD []

