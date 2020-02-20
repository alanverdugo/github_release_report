FROM python:3.8

# Install Python modules.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /requirements.txt

COPY report_releases.py /report_releases.py

CMD ["python", "/report_releases.py", "-h"]
