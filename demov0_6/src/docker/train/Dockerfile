FROM python:3.7-slim

USER root

COPY . /app

WORKDIR /app

RUN pip install -U scikit-learn==0.24.2 numpy argparse

ENTRYPOINT [ "python", "train.py" ]
