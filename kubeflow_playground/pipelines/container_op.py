import kfp
import kfp.dsl as dsl
import kfp.components as comp
from kubernetes.client.models import V1EnvVar

from kubeflow_playground.io import ARTIFACTS_DIR


def log_env_func():
    import os
    import logging

    logging.basicConfig(level=logging.INFO)
    env_variable = os.getenv("example_env")
    logging.info(f"The environment variable is: {env_variable=}")


def producer_op(text: str):
    # directly using ContainerOp is deprecated: https://github.com/kubeflow/pipelines/pull/4166
    return dsl.ContainerOp(
        name="producer",
        image="busybox",
        command=[
            "sh",
            "-c",
            f"echo {text} > /tmp/output.txt",
        ],
        file_outputs={"text-artifact": "/tmp/output.txt"},
    )


@comp.func_to_container_op
def expand_parameters(text: str) -> str:
    import json

    # dsl.ParallelFor requires JSON payload
    return json.dumps([c for c in text])


def consumer_op(text_artifact: str):
    return dsl.ContainerOp(
        name="consumer",
        image="busybox",
        command=["cat", (dsl.InputArgumentPath(text_artifact))],
    )


def consumer_func(text_artifact: str):
    for char in text_artifact:
        print(char)


consumer_func_op = comp.create_component_from_func(
    func=consumer_func,
    base_image="python:3.7",
)

log_env_func_op = comp.func_to_container_op(
    func=log_env_func,
    base_image="python:3.9",
)


@dsl.pipeline(name="artifact-passing-pipeline")
def artifact_passing_pipeline(text: str = "Hello world!", enable_fan_out: bool = False):
    env_var = V1EnvVar(name="example_env", value="env_variable")
    log_env_task = log_env_func_op().add_env_variable(env_var)

    producer_task = producer_op(text).after(log_env_task)
    text_artifact = producer_task.outputs["text-artifact"]
    consumer_task = consumer_op(text_artifact)
    consumer_func_task = consumer_func_op(text_artifact)
    with dsl.Condition(enable_fan_out == True):
        expansion_task = expand_parameters(text_artifact)
        with dsl.SubGraph(parallelism=1):
            with dsl.ParallelFor(expansion_task.output) as param:
                _ = consumer_func_op(param)


kfp.compiler.Compiler().compile(
    pipeline_func=artifact_passing_pipeline,
    package_path=str(ARTIFACTS_DIR / "container-op-pipeline.yaml"),
)
