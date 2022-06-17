from pydantic import BaseModel

class Rate(BaseModel):
    base: str
    date: str
    time_last_updated: int
    rates: dict

