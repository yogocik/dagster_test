from dagster import define_asset_job, AssetSelection
from src.resources.hooks import (create_failure_hook_via_slack, 
                                create_success_hook_via_slack,
                                create_skipped_hook_via_slack)

dummy_assets_job = define_asset_job(
    name='dummy_assets_job',
    selection= AssetSelection.groups("dummy"),
    description="Dummy Asset Materialization Job",
    tags={"env": "dev", "type": "dummy"},
    run_tags={"type": "dummy_job"},
    hooks={
        # create_failure_hook_via_slack(), 
        # create_success_hook_via_slack(), 
        create_skipped_hook_via_slack()
        }
)