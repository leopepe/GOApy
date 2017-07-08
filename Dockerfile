FROM ubuntu:latest

# app structure
RUN mkdir /app

# Install python3
# usefull extensions
RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    git \
    python3 \
    python3-dev \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools

RUN pip3 install \
    boto3==1.4. \
    botocore==1.5.14 \
    decorator==4.0.11 \
    docutils==0.13.1 \
    jmespath==0.9.1 \
    networkx==1.11 \
    python-dateutil==2.6.0 \
    s3transfer==0.1.10 \
    six==1.10.0 \
    git+https://github.com/leopepe/GOApy.git

WORKDIR /app
COPY examples/*.py /app

CMD ["python3", "cloud_builder.py"]