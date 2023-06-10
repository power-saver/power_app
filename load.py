import pymongo
import requests
import json
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
collection = db["power_usage_contract"]

city_collection = db["city_coordinates"]


# API URL 및 키 설정
api_key = "DppegJ028JUq9gaBiDk8LZHc6xSfFW4MT936vaRJ"
base_url = "https://bigdata.kepco.co.kr/openapi/v1/powerUsage/contractType.do"

with open('/user/city_coordinates/city_coordinates.json', 'r') as file:
    data = json.load(file)

# 데이터를 MongoDB에 저장합니다.
city_collection.insert_many(data)

# 연결을 닫습니다.

# # JSON 데이터 정리 함수
def clean_json_data(json_string):
    try:
        json_string = json_string.replace("}{", "},{")
        json_string = "[" + json_string + "]"
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# 2010년부터 2022년까지 데이터 가져오기
for year in range(2002, 2023):
    for month in range(1, 13):
        # API 호출
        params = {
            "returnType": "json",
            "apiKey": api_key,
            "year": format(year, '02'),
            "month": format(month, '02')
        }
        response = requests.get(base_url, params=params)
        # 불필요한 공백 및 줄바꿈 문자 제거
        response_text = response.text.strip()
        
        # JSON 형식으로 변환
        data = clean_json_data(response_text)
        items = data[1]["data"]
        if data is None:
            print(f"Error processing data for year {year} and month {month}")
            continue

        for item in items:
            collection.insert_one(item)
        # 진행 상황 출력
        print(f"Data imported for year {year} and month {month}")



print("데이터 가져오기 및 MongoDB에 저장 완료")
