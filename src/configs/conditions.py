from dagster import AutomationCondition
from src.configs.constants import TIMEZONE

def get_on_cron_condition(cron_schedule: str, 
                          timezone:str = TIMEZONE) -> AutomationCondition:
    return AutomationCondition.on_cron(cron_schedule=cron_schedule, 
                                       cron_timezone= timezone)

def get_passed_cron_condition(cron_schedule: str, 
                              timezone:str = TIMEZONE) -> AutomationCondition:
    return AutomationCondition.cron_tick_passed(cron_schedule=cron_schedule, 
                                                cron_timezone= timezone)
    
in_updated_or_requested_parents = AutomationCondition.any_deps_match(
    AutomationCondition.newly_updated() | AutomationCondition.newly_requested() 
)