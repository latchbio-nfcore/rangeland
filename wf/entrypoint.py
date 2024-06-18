from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: str, input_tar: typing.Optional[bool], dem: str, dem_tar: typing.Optional[bool], wvdb: str, wvdb_tar: typing.Optional[bool], data_cube: str, aoi: str, endmember: str, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], only_tile: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], sensors_level1: typing.Optional[str], sensors_level2: typing.Optional[str], start_date: typing.Optional[str], end_date: typing.Optional[str], resolution: typing.Optional[int], group_size: typing.Optional[int], force_threads: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('input_tar', input_tar),
                *get_flag('dem', dem),
                *get_flag('dem_tar', dem_tar),
                *get_flag('wvdb', wvdb),
                *get_flag('wvdb_tar', wvdb_tar),
                *get_flag('data_cube', data_cube),
                *get_flag('aoi', aoi),
                *get_flag('endmember', endmember),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('sensors_level1', sensors_level1),
                *get_flag('sensors_level2', sensors_level2),
                *get_flag('start_date', start_date),
                *get_flag('end_date', end_date),
                *get_flag('resolution', resolution),
                *get_flag('group_size', group_size),
                *get_flag('only_tile', only_tile),
                *get_flag('force_threads', force_threads),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_rangeland", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_rangeland(input: str, input_tar: typing.Optional[bool], dem: str, dem_tar: typing.Optional[bool], wvdb: str, wvdb_tar: typing.Optional[bool], data_cube: str, aoi: str, endmember: str, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], only_tile: typing.Optional[bool], multiqc_methods_description: typing.Optional[str], sensors_level1: typing.Optional[str] = 'LT04,LT05,LE07,S2A', sensors_level2: typing.Optional[str] = 'LND04 LND05 LND07', start_date: typing.Optional[str] = '1984-01-01', end_date: typing.Optional[str] = '2006-12-31', resolution: typing.Optional[int] = 30, group_size: typing.Optional[int] = 100, force_threads: typing.Optional[int] = 2) -> None:
    """
    nf-core/rangeland

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, input_tar=input_tar, dem=dem, dem_tar=dem_tar, wvdb=wvdb, wvdb_tar=wvdb_tar, data_cube=data_cube, aoi=aoi, endmember=endmember, outdir=outdir, email=email, multiqc_title=multiqc_title, sensors_level1=sensors_level1, sensors_level2=sensors_level2, start_date=start_date, end_date=end_date, resolution=resolution, group_size=group_size, only_tile=only_tile, force_threads=force_threads, multiqc_methods_description=multiqc_methods_description)

