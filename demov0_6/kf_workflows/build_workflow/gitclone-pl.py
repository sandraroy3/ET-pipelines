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
   name='Git clone pipeline',
   description='An example pipeline that clones a public repo'
)

#pipeline function
def pipeline_demo(
    # repo url 
    pipeline_repo_url='https://github.com/sandraroy3/ET-pipelines.git', # Public repo for now
    
    # TODO - have to test private repos
    # if your repo is private comment out the pipeline_repo_url above and uncomment the pipeline_repo_url below
    # pipeline_repo_url='https://${GIT_USERNAME}:${GIT_PASSWORD}@https://bitbkt.mdtc.itp01.p.fhlmc.com/scm/et/et-devops_for_datascience_im0220_ra4545.git',
    
    # name of your repo
    pipeline_repo_name='ET-pipelines'
    ):
    
    # Pipelines consists of steps and each component is defined as a function that returns an object of type ContainerOP, which comes from kfp sdk
    
    # step that git clones the repo with files
    git_clone_op = dsl.ContainerOp(
        name='Git clone Data',
        # the docker container image
        image='gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca',
        command=['bash','-c'],
        # git clone repo 
        arguments=[f'echo $(pwd) && echo $(ls) && git clone {pipeline_repo_url} && cd {pipeline_repo_name} && echo $(pwd)'],
        # connecting the volume to this container for persistent storage
        pvolumes={"/home/jovyan": dsl.PipelineVolume(pvc="modelstorage")}
    )
    git_clone_op.set_image_pull_policy("Always")

    # Gives the pipelines access to the secrets created from the create-secret.sh
#     dsl.get_pipeline_conf().set_image_pull_secrets([k8s_client.V1ObjectReference(name="bitbucket-creds")])

     # Step that builds and pushes the docker image.
    kaniko_op = dsl.ContainerOp(
        name='Kaniko step',
        # the docker container image
        image='gcr.io/arrikto/jupyter-kale-py36:develop-l0-release-1.2-pre-295-g622fe91aca',
        command=['bash','-c'],
        # starts kaniko pod to build and push docker image to registry
        arguments=[f'echo $(pwd) && echo $(ls) && cd {pipeline_repo_name} && '
                   'cd demov0_6 && cd kf_workflows && echo $(ls) && ./build_push_automate.sh'],
        # connecting the volume to this container for persistent storage
        pvolumes={"/home/jovyan": git_clone_op.pvolume}
    )
    # pull docker container image everytime do not use cache
    kaniko_op.set_image_pull_policy("Always")
 
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_demo, __file__ + '.zip')