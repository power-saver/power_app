from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..config.connection import MongoDBConnection


MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "power_usage_house"

mongo_conn = MongoDBConnection(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
collection = mongo_conn.get_collection()

router = APIRouter(
    prefix="/api/power-usage",
)

@router.get("/test")
def mogodb_test():  
    pipeline = [
    {
        '$group': {
            '_id': '$metro',
            'averagePowerUsage': { '$avg': '$powerUsage' }
        }
    }
    ]
    result = list(collection.aggregate(pipeline))
    return JSONResponse(status_code=200, content = result)


from fastapi import FastAPI


@router.get("")
def get_power_usage(myPowerUsage: str):
    myPower = myPowerUsage

    pipeline = [
    {
        '$group': {
            '_id': None,
            'averagePowerUsage': {'$avg': '$powerUsage'}
        }
    }
    ]

    # Aggregation 실행
    average_power  = list(collection.aggregate(pipeline))[0]["averagePowerUsage"]
    result = { "myPower" : myPower, "averagePower" : average_power}

    # print(result)
    print( "result" + str(result))
    return JSONResponse(status_code=200, content = result)
