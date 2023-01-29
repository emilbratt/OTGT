from pydantic import BaseModel
import json

class Raw(BaseModel):
    data: dict
    date: str

    CHECKS = [
        'pageId',
        'currency'
    ]

    def check(self, envar_get: object):
        for key in self.CHECKS:
            if key not in self.data.keys():
                return False
        return True

    def get_json_data(self) -> object:
        return json.dumps(self.data)

    def get_date(self) -> str:
        return self.date


class Reshaped(BaseModel):
    data: dict
    date: str
    region: str

    CHECKS = [
        'currency',
        'date',
        'unit',
        'max',
        'min',
        'average',
        'resolution',
        'prices',
    ]

    def check(self, envar_get: object):
        for key in self.CHECKS:
            if key not in self.data.keys():
                return False
        if len(self.data['prices']) < 1:
            return False
        return True

    def get_json_data(self) -> object:
        return json.dumps(self.data)

    def get_date(self) -> str:
        return self.date

    def get_region(self) -> str:
        return self.region
