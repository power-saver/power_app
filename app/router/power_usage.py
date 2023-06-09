from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..config.connection import MongoDBConnection
from ..service.power_usage_service import PowerUsageService
from ..model.power_usage_request import PowerUsageRequest

router = APIRouter(
    prefix="/api/power-usage",
)

powerUsageService = PowerUsageService()

@router.post("")
async def get_power_info(request: PowerUsageRequest):
    my_power_usage = request.myPowerUsage
    metro = request.metro
    city = request.city
    cntr = request.cntr
    year = str(format(int(request.year),'02'))
    month = str(format(int(request.month),'02'))

    power_usage_average = powerUsageService.get_average_power_usage(metro, city, cntr, year, month)
    previous_year_average_power = powerUsageService.get_average_power_usage(metro, city, cntr, str(int(year) - 1), month)
    neighbor_city_list = powerUsageService.get_neighbor_city_power_usage_list(metro, city, cntr, year, month)
    top_city_list = powerUsageService.get_top_city_power_usage_list(cntr, year, month)
    cntr_list = powerUsageService.get_power_by_cntr(metro, city, year, month)
    costList =  powerUsageService.get_my_city_cost(my_power_usage, metro, city, cntr, year, month)
    if power_usage_average is None:
        return JSONResponse(status_code=404, content={"message": "404 Not Found."})
    
    response = {
            "myPower": my_power_usage,
            "averagePower": power_usage_average,
            "powerRatio": float(powerUsageService.get_ratio(power_usage_average, float(my_power_usage))),
            "prevAveragePower": previous_year_average_power,
            "neighborCityList" : neighbor_city_list,
            "topCityList" : top_city_list,
            "cntrList": cntr_list,
            "myCityCost" : costList[0],
            "myCost" : costList[1]
        }
    return response

    
# /api/power-usage?myPowerUsage=400&metro=서울특별시&city=성동구&cntr=교육용&year=2018&month=11