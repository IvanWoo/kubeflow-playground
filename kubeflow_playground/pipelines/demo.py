import kfp
import kfp.components as comp
import kfp.dsl as dsl

from kubeflow_playground.io import ARTIFACTS_DIR


def merge_csv(file_path: comp.InputPath("Tarball"), output_csv: comp.OutputPath("CSV")):
    import glob
    import pandas as pd
    import tarfile

    tarfile.open(name=file_path, mode="r|gz").extractall("data")
    df = pd.concat(
        [pd.read_csv(csv_file, header=None) for csv_file in glob.glob("data/*.csv")]
    )
    df.to_csv(output_csv, index=False, header=False)


create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    output_component_file=str(
        ARTIFACTS_DIR / "demo-component.yaml"
    ),  # This is optional. It saves the component spec for future use.
    base_image="python:3.7",
    packages_to_install=["pandas==1.1.4"],
)

web_downloader_op = kfp.components.load_component_from_url(
    "https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml"
)


@dsl.pipeline(
    name="demo pipeline",
    description="A demo pipeline.",
)
def my_pipeline(url: "URI"):
    web_downloader_task = web_downloader_op(url=url)
    merge_csv_task = create_step_merge_csv(file=web_downloader_task.outputs["data"])
    # The outputs of the merge_csv_task can be referenced using the
    # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']


kfp.compiler.Compiler().compile(
    pipeline_func=my_pipeline, package_path=str(ARTIFACTS_DIR / "demo-pipeline.yaml")
)
