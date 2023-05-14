from fastapi import FastAPI
from .router import power_usage


app = FastAPI()
app.include_router(power_usage.router)

@app.get("/")
def read_root():
    return {"ping"}