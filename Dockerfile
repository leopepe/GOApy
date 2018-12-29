FROM python:3

# app structure
RUN mkdir /app

COPY . /app

WORKDIR /app

RUN python setup.py install

#CMD ["python3", "cloud_builder.py"]