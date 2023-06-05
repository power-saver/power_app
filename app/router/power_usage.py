from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..config.connection import MongoDBConnection
from ..service import power_usage_service

router = APIRouter(
    prefix="/api/power-usage",
)

powerUsageService = power_usage_service.PowerUsageService()

@router.get("")
def get_power_info(
        myPowerUsage: str,
        metro: str,
        city: str,
        cntr: str,
        year: str,
        month: str
):
    power_usage_average = powerUsageService.get_average_power_usage(metro, city, cntr, year, month)
    previous_year_average_power = powerUsageService.get_average_power_usage(metro, city, cntr, str(int(year) - 1), month)


    if power_usage_average is None:
        return JSONResponse(status_code=404, content={"message": "404 Not Found."})
    
    response = {
            "myPower": myPowerUsage,
            "averagePower": power_usage_average,
            "power_ratio": float(powerUsageService.get_ratio(power_usage_average, float(myPowerUsage))),
            "prevAveragePower": previous_year_average_power,
        }
    return response


# /api/power-usage?myPowerUsage=400&metro=서울특별시&city=성동구&cntr=교육용&year=2018&month=11