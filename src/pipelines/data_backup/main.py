from dagster import Definitions, load_assets_from_modules, ExperimentalWarning as DagsterExperimentalWarning
from src.pipelines.data_backup.assets import dummy as dummy_backup_assets
from src.resources.dummy import DummyResource
import warnings

warnings.filterwarnings("ignore", category=DagsterExperimentalWarning)

backup_dummy_assets = load_assets_from_modules([dummy_backup_assets])

defs = Definitions(assets=backup_dummy_assets,
                   resources= {
                       'conn': DummyResource(name='dummy_resources')
                   })
