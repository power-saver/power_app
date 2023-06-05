from pydantic import BaseModel
class PowerUsageRequest(BaseModel):
    myPowerUsage: str
    metro: str
    city: str
    cntr: str
    year: str
    month: str