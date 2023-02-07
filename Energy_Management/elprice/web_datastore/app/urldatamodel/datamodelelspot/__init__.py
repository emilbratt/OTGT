from pydantic import BaseModel
import json

class Raw_v0(BaseModel):
    data: dict
    date: str

    def check(self, envar_get: object):
        CHECKS = [
            'pageId',
            'currency'
        ]
        for key in CHECKS:
            if key not in self.data.keys():
                return False
        return True

    def get_json_data(self) -> object:
        return json.dumps(self.data)

    def get_date(self) -> str:
        return self.date

class Reshaped_v0(BaseModel):
    data: dict
    date: str
    region: str

    def check(self, envar_get: object):
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
        for key in CHECKS:
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

class Reshaped_v1(BaseModel):
    data: list
    date: str

    def check(self, envar_get: object):
        CHECKS = [
            'region',
            'date',
            'currency',
            'unit',
            'max',
            'min',
            'average',
            'resolution',
            'prices',
        ]
        for key in CHECKS:
            for region_data in self.data:
                if key not in region_data.keys():
                    return False
            if len(region_data['prices']) == 0:
                return False
        return True

    def get_json_data(self) -> object:
        return json.dumps(self.data)

    def get_date(self) -> str:
        return self.date
