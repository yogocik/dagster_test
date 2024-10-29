from dagster import (asset, 
                     AssetExecutionContext, 
                     BackfillPolicy, 
                     RetryPolicy,
                     AssetCheckSpec,
                     Output,
                     AssetCheckResult,
                     AssetCheckSeverity,
                     Config,
                     AssetIn,
                     AssetKey)
from typing import Any, Dict, Optional
from src.configs.partitions import DUMMY_ASSET_DAILY_PARTITION
from src.configs.constants import (DUMMY_ASSET_GROUP_NAME, 
                                   PYTHON_COMPUTE_KIND, 
                                   ANONYM,
                                   MAX_PARTITIONS_PER_RUN,
                                   MAX_RETRIES,
                                   CRON_SCHEDULE,
                                   RETRY_DELAY_IN_SEC)
from src.configs.conditions import get_on_cron_condition
from random import randint


@asset(
    name='asset_1',
    key_prefix='dummy',
    group_name=DUMMY_ASSET_GROUP_NAME,
    partitions_def= DUMMY_ASSET_DAILY_PARTITION,
    tags={'type': 'dummy', 'env': 'dev'},
    required_resource_keys= {'conn'},
    kinds={PYTHON_COMPUTE_KIND},
    owners=[ANONYM, 'team:personal'],
    automation_condition= get_on_cron_condition(CRON_SCHEDULE),
    backfill_policy= BackfillPolicy.multi_run(max_partitions_per_run=MAX_PARTITIONS_PER_RUN),
    retry_policy= RetryPolicy(max_retries=MAX_RETRIES, 
                              delay=RETRY_DELAY_IN_SEC),
    check_specs=[AssetCheckSpec(name='non_empty_data', 
                                asset=AssetKey(['dummy', 'asset_1'])
                                ),
                 AssetCheckSpec(name='list_data_format', 
                                asset=AssetKey(['dummy', 'asset_1'])
                                )
                ]
)
def predefined_dummy_asset(context: AssetExecutionContext) -> Dict[str, Any]:
    # number = randint(1,2)
    number = 1
    
    data = context.resources.conn.get_dummy_data(data=[1,2,3]) if number % 2 == 0 else None # If even, it will be None
    
    context.log.info(f"Asset Partition Key: {context.partition_key}")
    
    # Check asset (non_empty_data)
    yield AssetCheckResult(
        check_name='non_empty_data',
        asset_key= context.asset_key,
        severity= AssetCheckSeverity.WARN,
        metadata = {"data": data},
        passed=bool(len(data.get("data"))) if isinstance(data, dict) else False
    )
    
    # Check asset (list_data_format)
    yield AssetCheckResult(
        check_name='list_data_format',
        asset_key= context.asset_key,
        severity= AssetCheckSeverity.WARN,
        metadata = {'type': str(type(data.get("data")) if isinstance(data, dict) else data), 'whole_type': str(type(data))},
        passed=  isinstance(data.get("data"), list) if isinstance(data, dict) else False
    )
    
    # Return value
    yield Output(value=data, output_name='result')


class MultiplierAssetConfig(Config):
    multiplier: int = 2


@asset(
    name='asset_2',
    key_prefix='dummy',
    description="Multiply first asset of dummy 1",
    group_name=DUMMY_ASSET_GROUP_NAME,
    partitions_def= DUMMY_ASSET_DAILY_PARTITION,
    tags={'type': 'dummy', 'env': 'dev'},
    kinds={PYTHON_COMPUTE_KIND},
    ins={
        "upstream_asset": AssetIn(key=AssetKey(['dummy', 'asset_1']))
        },
    owners=[ANONYM, 'team:personal'],
    automation_condition= get_on_cron_condition("0 8 * * *"),
    backfill_policy= BackfillPolicy.multi_run(max_partitions_per_run=MAX_PARTITIONS_PER_RUN),
    retry_policy= RetryPolicy(max_retries=MAX_RETRIES, 
                              delay=RETRY_DELAY_IN_SEC),
    check_specs=[AssetCheckSpec(name='existed_data', 
                                asset=AssetKey(['dummy', 'asset_2'])
                                ),
                 ],
    output_required=False
)
def processed_dummy_asset(context: AssetExecutionContext, 
                          config: MultiplierAssetConfig,
                          upstream_asset) -> list[int] | None:
    context.log.info(f"Processed Asset Run : {context.run_id}")
    multiplier = config.multiplier
    context.log.info(f"Upstream Asset : {upstream_asset}")
    data = []
    if isinstance(upstream_asset, dict):
        data = upstream_asset.get("data") * multiplier
        yield Output(value=data, 
                     output_name='result')
    context.log.info(f"Processed data : {data}")    
    # Check asset (data multiplication)
    yield AssetCheckResult(
        check_name='existed_data',
        asset_key= context.asset_key,
        severity= AssetCheckSeverity.WARN,
        metadata = {"data": data, "source": upstream_asset},
        passed=bool(data)
    )

@asset(
    name='asset_3',
    key_prefix='dummy',
    description="Display multiplication of dummy 1",
    group_name=DUMMY_ASSET_GROUP_NAME,
    partitions_def= DUMMY_ASSET_DAILY_PARTITION,
    tags={'type': 'dummy', 'env': 'dev'},
    kinds={PYTHON_COMPUTE_KIND},
    ins={
        "upstream": AssetIn(key=AssetKey(['dummy', 'asset_2']))
        },
    owners=[ANONYM, 'team:personal'],
    automation_condition= get_on_cron_condition("15 8 * * *"),
    backfill_policy= BackfillPolicy.multi_run(max_partitions_per_run=MAX_PARTITIONS_PER_RUN),
    retry_policy= RetryPolicy(max_retries=MAX_RETRIES, 
                              delay=RETRY_DELAY_IN_SEC),
    output_required=False
)
def displayed_dummy_asset(context: AssetExecutionContext,
                          upstream) -> None:
    context.log.info(f"Upstream Asset Value : {upstream}")