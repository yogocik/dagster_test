from dagster import ConfigurableResource
from typing import Dict, Any

class DummyResource(ConfigurableResource):
    name: str 
    
    def get_dummy_data(self,data: Any) -> Dict[str,Any]:
        return {
            "data": data
        }
        