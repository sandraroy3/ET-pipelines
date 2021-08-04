# FROM gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca
FROM python:3.7-slim

USER root

# get training code
COPY . /app

# assemble model specific components required for training
WORKDIR /app



# set current working directory for the training
# WORKDIR /app/preprocess


RUN pip install -U scikit-learn==0.24.2 numpy 

ENTRYPOINT [ "python", "preprocess.py" ]