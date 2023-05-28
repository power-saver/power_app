from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..config.connection import MongoDBConnection

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "power_usage_contract"

mongo_conn = MongoDBConnection(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
collection = mongo_conn.get_collection()

router = APIRouter(
    prefix="/api/power-usage",
)


def get_average_power_usage(metro: str, city: str, cntr: str, year: str, month: str):
    document = collection.find_one({
        'metro': metro,
        'city': city,
        'cntr': cntr,
        'year': year,
        'month': month
    })

    if document:
        power_usage = document['powerUsage']
        cust_count = document['custCnt']
        average_power_usage = power_usage / cust_count
        return average_power_usage
    else:
        return None
    
def get_ratio(a: float, b: float):
    change = b - a
    ratio = (change / a) * 100
    return ratio


@router.get("")
def get_power_info(
        myPowerUsage: float,
        metro: str,
        city: str,
        cntr: str,
        year: str,
        month: str
):
    current_average_power = get_average_power_usage(metro, city, cntr, year, month)
    previous_year_average_power = get_average_power_usage(metro, city, cntr, str(int(year) - 1), month)

    if current_average_power is not None:
        power_ratio = get_ratio(myPowerUsage, current_average_power)

        response = {
            "myPower": myPowerUsage,
            "averagePower": current_average_power,
            "power_ratio": int(power_ratio),
            "previousYearAveragePower": previous_year_average_power,
        }
        return JSONResponse(status_code=200, content=response)
    else:
        return JSONResponse(status_code=404, content={"message": "404 Not Found."})


# /api/power-usage?myPowerUsage=400&metro=서울특별시&city=성동구&cntr=교육용&year=2018&month=11
# uvicorn app.main:app --port 8080