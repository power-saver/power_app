import math
import json

def calculate_distance(lat1, lon1, lat2, lon2):
    # 위도 및 경도를 라디안 단위로 변환
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # 경도 및 위도의 차이 계산
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # 구면 코사인 법칙을 사용하여 거리 계산
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # 지구 반경 6371km 사용

    return distance

def find_nearest_cities(target_lat, target_lon, cities, num_results=5):
    distances = []
    
    # 모든 도시와의 거리 계산
    for city in cities:
        city_lat = city["Latitude"]
        city_lon = city["Longitude"]
        distance = calculate_distance(target_lat, target_lon, city_lat, city_lon)
        distances.append((city["City"], distance))
    
    # 거리를 기준으로 오름차순 정렬
    distances.sort(key=lambda x: x[1])
    
    # 최단거리의 도시 추출
    nearest_cities = [city[0] for city in distances[:num_results]]
    
    return nearest_cities

def read_city_coordinates_from_file(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data

# city_coordinates.json 파일 경로
file_path = "city_coordinates/city_coordinates.json"

# 파일에서 도시 데이터 읽어오기
city_coordinates = read_city_coordinates_from_file(file_path)

# # 테스트용 타겟 위치
# target_lat = 37.5
# target_lon = 127.0

my_city = input()

target_lat = 

# 최단거리의 도시 추출
nearest_cities = find_nearest_cities(target_lat, target_lon, city_coordinates, num_results=5)

# 최단거리의 도시 출력
print(nearest_cities)