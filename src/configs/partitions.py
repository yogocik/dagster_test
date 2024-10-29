from dagster import (DailyPartitionsDefinition, 
                     HourlyPartitionsDefinition, 
                     WeeklyPartitionsDefinition, 
                     MonthlyPartitionsDefinition, 
                     DynamicPartitionsDefinition)
from src.configs.constants import DUMMY_START_DATE, TIMEZONE, CRON_SCHEDULE

DUMMY_ASSET_DAILY_PARTITION = DailyPartitionsDefinition(start_date=DUMMY_START_DATE,
                                                        cron_schedule= CRON_SCHEDULE,
                                                        timezone=TIMEZONE,)

DUMMY_ASSET_HOURLY_PARTITION = HourlyPartitionsDefinition(start_date=f'{DUMMY_START_DATE}-00:00',
                                                          cron_schedule= "50 * * * *",
                                                          timezone=TIMEZONE,)