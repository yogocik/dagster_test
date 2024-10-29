from dagster_slack import slack_resource
import os

SLACK_RESOURCE = slack_resource.configured(
    {
        "token": os.getenv("SLACK_TOKEN")
    }
) # Nanodata slack connection