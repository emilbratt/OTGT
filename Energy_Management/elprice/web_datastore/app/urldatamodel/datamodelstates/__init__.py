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
            'region',
        ]
        for key in CHECKS:
            if key not in self.data.keys():
                return False
        return True

    def get_json_data(self) -> object:
        return json.dumps(self.data)
