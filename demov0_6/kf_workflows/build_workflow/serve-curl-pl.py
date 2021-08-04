from kubernetes import client as k8s_client
import kfp
import json
from string import Template
from kfp_server_api.models import *
import getpass
from kfp.onprem import use_k8s_secret
import kfp.dsl as dsl

# this module is a using kfp sdk to clone a repo then docker builds and pushes an image(s) to a docker registry
@dsl.pipeline(
   name='Serve and curl using a volume',
   description='An example pipeline that serves a model and tests it with curl'
)

#pipeline function
def pipeline_demo(
    # repo url 
#     pipeline_repo_url='https://github.com/ettynan/emerging.git', # Public repo for now
    
#     # TODO - have to test private repos
#     # if your repo is private comment out the pipeline_repo_url above and uncomment the pipeline_repo_url below
#     # pipeline_repo_url='https://${GIT_USERNAME}:${GIT_PASSWORD}@https://bitbkt.mdtc.itp01.p.fhlmc.com/scm/et/et-devops_for_datascience_im0220_ra4545.git',
    
#     # name of your repo
    pipeline_repo_name='ET-pipelines'
    ):
    
    # volume created to pass artifacts between docker containers
#     vop = dsl.VolumeOp(
#         name = "Pipeline Volume",
#         resource_name = "pipelinePvc",
#         # need storage_class = "standard" since by default it is rok and the pod won't mount with the volume currently.
#         storage_class = "standard",
#         size = "3Gi",        
#         # The volume can be mounted as read-write by a single node
#         modes = dsl.VOLUME_MODE_RWO
#     )
    
    # Pipelines consists of steps and each component is defined as a function that returns an object of type ContainerOP, which comes from kfp sdk
     
    # Step that serves a model using Kfserving. Will get an inferenceservice deployed.
    serve_op = dsl.ContainerOp(
        name='Serve step',
        # the docker container image
        image='gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca',
        command=['bash','-c'],
        # starts kaniko pod to serve a model using kfserving.
        arguments=[f'echo $(pwd) && echo $(ls) && cd {pipeline_repo_name} && '
                   'kubectl apply -f sklearn-irisv2.yaml'],
        # connecting the volume to this container for persistent storage
        pvolumes={"/home/jovyan": dsl.PipelineVolume(pvc="modelstorage")}
    )
    # pull docker container image everytime do not use cache
    serve_op.set_image_pull_policy("Always")

    # Step that test the inferenceservice deployed can return predictions once input data is passed to it.
    testcurl_op = dsl.ContainerOp(
        name='Test Curl step',
        # the docker container image
        image='gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca',
        command=['bash','-c'],
        # starts kaniko pod to run a test_curl.sh file to get back predictions
        arguments=[f'echo $(pwd) && echo $(ls) && cd {pipeline_repo_name} && echo $(ls) && ' 
                   'bash test_curl_v2.sh'],
        # connecting the volume to this container for persistent storage
        pvolumes={"/home/jovyan": serve_op.pvolume}
    )
    # pull docker container image everytime do not use cache
    testcurl_op.set_image_pull_policy("Always")

    # Gives the pipelines access to the secrets created from the create-secret.sh
#     dsl.get_pipeline_conf().set_image_pull_secrets([k8s_client.V1ObjectReference(name="bitbucket-creds")])
 
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_demo, __file__ + '.zip')