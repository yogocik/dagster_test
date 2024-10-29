from dagster import Definitions, load_assets_from_modules, ExperimentalWarning as DagsterExperimentalWarning
from src.pipelines.airbyte_staging.assets import dummy as dummy_airbyte_assets
from src.pipelines.airbyte_staging.pipes.dummy import dummy_assets_job
from src.pipelines.airbyte_staging.triggers.dummy_schedule import dummy_asset_job_schedule
from src.resources.dummy import DummyResource
from src.resources.slack import SLACK_RESOURCE
import warnings
import dagster_gcp

warnings.filterwarnings("ignore", category=DagsterExperimentalWarning)

airbyte_dummy_assets = load_assets_from_modules([dummy_airbyte_assets])

defs = Definitions(assets=airbyte_dummy_assets,
                   jobs=[dummy_assets_job],
                   schedules=[dummy_asset_job_schedule],
                   resources= {
                       'conn': DummyResource(name='dummy_resources'),
                       'slack': SLACK_RESOURCE
                   })
