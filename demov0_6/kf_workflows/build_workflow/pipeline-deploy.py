# execute this script, then navigate to Kubeflow Central dash->Pipelines->Experiments
from kubernetes import client as k8s_client
import kfp.dsl as dsl
import json
from string import Template

@dsl.pipeline(
   name='Iris model Pipeline',
   description='An example pipeline that trains and logs a regression model.'
)

def pipeline_demo(    
    
    ):    
  # volume created to pass artifacts between docker containers
#     vop = dsl.VolumeOp(
#         name = "Pipeline Volume",
#         resource_name = "pipelinePvc",
#         storage_class = "standard",
#         size = "3Gi",
#         # The volume can be mounted as read-write by a single node
#         modes = dsl.VOLUME_MODE_RWO
#     )
    
# each component is defined as a function that returns an object of type ContainerOP, which comes from kfp sdk
    preprocess_op = dsl.ContainerOp(
        name='Preprocess Data',
        image='sandraroy3/preprocess:v11',
        command=['python'],
        arguments=[
            'preprocess.py'
        ],
        pvolumes={'/home/jovyan':  dsl.PipelineVolume(pvc="modelstorage")}
    )
    preprocess_op.set_image_pull_policy("Always")
    
    
    train_op = dsl.ContainerOp(
        name='Train Model',
        image='sandraroy3/train:v11',
        command=['python'],
        arguments=[
            'train.py',
            '--x_train', '/home/jovyan/x_train.npy',
            '--y_train', '/home/jovyan/y_train.npy',
            '--model_path', '/home/jovyan'
        ],
        pvolumes={'/home/jovyan': preprocess_op.pvolume}
    )
    train_op.set_image_pull_policy("Always")

    
    test_op = dsl.ContainerOp(
        name='Test Model',
        image='sandraroy3/test:v11',
        command=['python'],
        arguments=[
            'test.py',
            '--x_test', '/home/jovyan/x_test.npy',
            '--y_test', '/home/jovyan/y_test.npy',
            '--model', '/home/jovyan/model.joblib',
            '--output_path', '/home/jovyan',
        ],
        pvolumes={'/home/jovyan': train_op.pvolume}
#         arguments=[
#             '--x_test', dsl.InputArgumentPath(preprocess_op.outputs['x_test']),
#             '--y_test', dsl.InputArgumentPath(preprocess_op.outputs['y_test']),
#             '--model', dsl.InputArgumentPath(train_op.outputs['model'])
#         ],
#         # TODO - output is not a meansqerror but a prediction
#         file_outputs={
#             'mean_squared_error': '/app/output.txt'
#         }
    )    
    test_op.set_image_pull_policy("Always") 
    
#applys to pipeline as whole
#dsl.get_pipeline_conf().set_image_pull_secrets([k8s_client.V1ObjectReference(name="dockersecret")])
   
    
if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline_demo, __file__ + '.zip')
