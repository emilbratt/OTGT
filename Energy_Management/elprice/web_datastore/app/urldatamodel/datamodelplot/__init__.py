from pydantic import BaseModel

class ByDate_v0(BaseModel):
    region: str
    date: str
    data: str

class ByHour_v0(BaseModel):
    region: str
    date: str
    index: int
    hour: int
    data: str
