FROM apache/beam_python3.11_sdk:2.49.0

COPY . ./

RUN pip install --no-cache-dir requirements.txt

