FROM tiangolo/uvicorn-gunicorn:python3.7

# RUN apt-get clean && apt-get update && apt-get install -y libpq-dev python3-dev
RUN apt-get update && apt-get install -y python3-opencv

COPY requirements.txt /tmp/requirements.txt

RUN pip install -U pip
RUN python3 -m pip install -v --no-cache-dir -r /tmp/requirements.txt
RUN python -m pip install -U scikit-learn

RUN mkdir -p /var/log/kupintar

WORKDIR /app