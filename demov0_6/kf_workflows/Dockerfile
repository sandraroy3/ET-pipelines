# Docker2 would be the one with exporting model
# base img would be docker1 ie kfservingsklearn or seldonio img

FROM seldonio/mlserver:0.2.1

# copy exported model to image
ARG EXPORTED_MODEL
WORKDIR /model
COPY $EXPORTED_MODEL /model/$EXPORTED_MODEL

# To build this docker2 image with model passed as a build arg
docker build \
  --build-arg EXPORTED_MODEL=diabetes_model.pkl \
  -t diabetes_model -f Dockerfile .