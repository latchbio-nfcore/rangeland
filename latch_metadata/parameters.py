
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description='Root directory of all sattelite imagery.',
    ),
    'input_tar': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Indicates whether input is a tar archive.',
    ),
    'dem': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Digital elevation model.',
    ),
    'dem_tar': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Indicates whether dem is a tar archive.',
    ),
    'wvdb': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Water vapor dataset.',
    ),
    'wvdb_tar': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Indicates whether wvdb is a tar archive.',
    ),
    'data_cube': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Datacube definition.',
    ),
    'aoi': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Area of interest.',
    ),
    'endmember': NextflowParameter(
        type=str,
        default=None,
        section_title=None,
        description='Endmember definition.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'sensors_level1': NextflowParameter(
        type=typing.Optional[str],
        default='LT04,LT05,LE07,S2A',
        section_title='Remote sensing image options',
        description='Satellites for which first level data should be processed.',
    ),
    'sensors_level2': NextflowParameter(
        type=typing.Optional[str],
        default='LND04 LND05 LND07',
        section_title=None,
        description='Satellites for which data should be incorporated into higher level processing.',
    ),
    'start_date': NextflowParameter(
        type=typing.Optional[str],
        default='1984-01-01',
        section_title=None,
        description='First day of interest.',
    ),
    'end_date': NextflowParameter(
        type=typing.Optional[str],
        default='2006-12-31',
        section_title=None,
        description='Last day of interest.',
    ),
    'resolution': NextflowParameter(
        type=typing.Optional[int],
        default=30,
        section_title=None,
        description='Spatial resolution applied in analyses.',
    ),
    'group_size': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title='Workflow configuration',
        description='Batch size of  tiles considered for merging.',
    ),
    'only_tile': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Controls wheter spectral unmixing is applied in higher level processing..',
    ),
    'force_threads': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title='FORCE parameters',
        description='Number of threads spawned by FORCE for each higher-level or preprocessing task.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

