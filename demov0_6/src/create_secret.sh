#!/bin/bash

read -p "Enter Your github username: " id
read -s -p "Enter Your Github Password: " gh_password
read -s -p "Enter Your Dockerhub Password: " dh_password
read -p "Enter Your email-id associated with your dockerhub account: " emailid

kubectl delete secret github-creds
kubectl delete secret docker-creds

# secret to use dockerhub registry - https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
kubectl create secret docker-registry docker-creds --docker-server=https://index.docker.io/v2/ --docker-username=${id} --docker-password=${dh_password} --docker-email=${emailid}

# that authenticates you to your github repo (need this to if you are cloning from a private github repo).
kubectl create secret generic github-creds \
--from-literal="GIT_USERNAME=${id}" \
--from-literal="GIT_PASSWORD=${gh_password}"