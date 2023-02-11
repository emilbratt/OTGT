from pydantic import BaseModel
import json

class ByDate_v0(BaseModel):
    region: str
    date: str
    data: dict

    def check(self, envar_get: object):
        CHECKS = [
            'region',
            'date',
        ]
        for key in CHECKS:
            for region_data in self.data:
                if key not in region_data.keys():
                    return False
        return True

    def get_json_data(self) -> object:
        return json.dumps(self.data)
