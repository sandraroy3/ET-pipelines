# FROM gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca
FROM python:3.7-slim

USER root

COPY . /app

WORKDIR /app

RUN pip install -U scikit-learn==0.24.2 numpy argparse

ENTRYPOINT [ "python", "test.py" ]
