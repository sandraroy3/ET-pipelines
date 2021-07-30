#!/bin/bash
set -xe

INPUT_PATH="@./iris-input.json"
MODEL_SERVICE_NAME="sklearn-irisv2"
MODEL_SERVICE_IP_ADDR=$(kubectl get svc -l serving.kubeflow.org/inferenceservice=${MODEL_SERVICE_NAME},networking.internal.knative.dev/serviceType=Private -o jsonpath='{.items[0].spec.clusterIP}')
MODEL_SERVICE_PORT=$(kubectl get svc -l serving.kubeflow.org/inferenceservice=${MODEL_SERVICE_NAME},networking.internal.knative.dev/serviceType=Private -o jsonpath='{.items[0].spec.ports[0].port}')



echo -e input_path ${INPUT_PATH} "\n"
echo -e model_service_name ${MODEL_SERVICE_NAME} "\n"
echo -e model_service_ip_addr ${MODEL_SERVICE_IP_ADDR} "\n"
echo -e mode_service_post ${MODEL_SERVICE_PORT} "\n"


curl -v -k -L \
    -H "kubeflow-userid: user" \
    http://${MODEL_SERVICE_IP_ADDR}:${MODEL_SERVICE_PORT}/v2/models/${MODEL_SERVICE_NAME}/infer -d ${INPUT_PATH}
