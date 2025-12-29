import os
from pathlib import Path
from dagster_dbt import DbtCliResource, dbt_assets  
from dagster_airbyte import AirbyteResource
from dagster_airbyte import load_assets_from_airbyte_instance

AIRBYTE_WORKSPACE_ID = "d761582d-1a87-4bff-8d8f-7ccc15fc5ebf"

resources = {
    "dbt": DbtCliResource(
        project_dir=os.getenv("DBT_PROJECT_DIR"),
    ),
    "airbyte_instance": AirbyteResource (
        host="localhost",
        port="8000",
        # If using basic auth, include username and password:
        username=os.getenv("AIRBYTE_USERNAME", "admin"),
        password=os.getenv("AIRBYTE_PASSWORD")
    )
}

manifest_path = Path(os.getenv("DBT_PROJECT_DIR")) / "target" / "manifest.json"

@dbt_assets(manifest=manifest_path)
def dbt_transformation_assets(context, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

airbyte_assets = load_assets_from_airbyte_instance(
    resources["airbyte_instance"], 
    workspace_id=AIRBYTE_WORKSPACE_ID, 
    key_prefix=["raw_data"]
)