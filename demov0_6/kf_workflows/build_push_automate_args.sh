#!/bin/bash

# dockerfile base image
dockerfile_base_image="gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca"

# Insert names of all folders in the Docker folder with a " " in between each name (ex. all_steps="preprocess train test")
all_steps="preprocess train test" 

# Working directory to be used for image creation
working_directory="ET-pipelines/demov0_6"

# Private dockerhub registry url
server_url="index.docker.io"

# your dockerhub username for craeting repository
repository="sandraroy3"

# version of the image
version_number="v12"

# name of your workspace volume
notebook_claimName="workspace-jkfserving-cp4jqhrhm" 

# secret for pushing to dockerhub artifactory
docker_secret="san-docker-creds"

