from dagster import DefaultScheduleStatus, ScheduleDefinition
from src.pipelines.airbyte_staging.pipes.dummy import dummy_assets_job

dummy_asset_job_schedule = ScheduleDefinition(
    name = 'dummy_job_schedule',
    cron_schedule="30 7 * * *",
    execution_timezone='Asia/Jakarta',
    description='Schedule for dummy asset materialization job',
    default_status= DefaultScheduleStatus.STOPPED,
    job=dummy_assets_job
)