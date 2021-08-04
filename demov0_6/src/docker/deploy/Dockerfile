FROM python:3.7-slim

WORKDIR /app

RUN pip install argparse

COPY deploy.py ./deploy.py

ENTRYPOINT [ "python", "deploy.py" ]
