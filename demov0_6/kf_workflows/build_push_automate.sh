#!/bin/bash

# calling the args from the build_push_automate_args.sh file to fill in below
source build_push_automate_args.sh

# for loop that creates image for each folder listed in the all_steps 
for current_step in $all_steps
do
    # the name you want to give the image
    image_name="${current_step}"

    # path to Dockerfile 
    path_to_dockerfile="${working_directory}/src/docker/${current_step}/Dockerfile"

    # folder path to where Dockerfile is situated
    folder_dockerfile_is_in="${working_directory}/src/docker/${current_step}" 

    # Copies content of build-template with env variables to create build-final.yaml
    rm -f build_final.yaml 
    (echo "cat <<EOF >build_final.yaml";                               
      cat build_template.yaml;
    ) >temp.yml          
    . temp.yml            
    rm temp.yml

    # deletes existing pod(s)
    kubectl delete pod kf-pipelines-${current_step} 

    # applies build-final.yaml to start pod in your kubernetes namespace.
    kubectl apply -f build_final.yaml 
    
    #deletes file to keep repo clean comment out if you want to debug the yaml file created
    rm -f build_final.yaml 
    
done