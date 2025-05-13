# modules/osm_service.py

import requests
from math import sqrt
from modules.utils import create_geojson_circle, get_bounding_box_from_polygon

# Danh sách các loại đường không muốn lấy (giống trong api.js)
HIGHWAY_EXCLUDE = ["footway", "street_lamp", "steps", "pedestrian", "track", "path"]

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

def build_overpass_query(bounding_box):
    """
    Tạo truy vấn Overpass QL từ bounding box.
    bounding_box: [southwest: {"latitude", "longitude"}, northeast: {"latitude", "longitude"}]
    """
    exclusion = "".join([f'[highway!="{e}"]' for e in HIGHWAY_EXCLUDE])

    query = f"""
    [out:json];
    (
        way[highway]{exclusion}[footway!="*"]
        ({bounding_box[0]["latitude"]},{bounding_box[0]["longitude"]},
         {bounding_box[1]["latitude"]},{bounding_box[1]["longitude"]});
        node(w);
    );
    out skel;
    """
    return query


def fetch_overpass_data(bounding_box):
    """
    Gửi truy vấn Overpass API để lấy dữ liệu đường đi và node trong bounding box.
    Trả về JSON.
    """
    query = build_overpass_query(bounding_box)
    response = requests.post(OVERPASS_API_URL, data=query)
    response.raise_for_status()
    return response.json()

def get_nearest_node(lat, lon, radius_deg=0.15):
    """
    Tìm node OSM gần nhất với tọa độ (lat, lon), đảm bảo node nằm trên các đường hợp lệ.
    """
    # 1. Tạo polygon vòng tròn
    circle = create_geojson_circle(lat, lon, radius_km=radius_deg * 111)  # approx km
    polygon = circle["coordinates"][0]

    # 2. Tính bounding box
    bbox = get_bounding_box_from_polygon(polygon)

    # 3. Truy vấn Overpass API để lấy node thuộc các đường highway hợp lệ
    map_data = fetch_overpass_data(bbox)

    # 4. Tìm node gần nhất trong dữ liệu đã lọc
    result = None
    result_dist = float("inf")

    for element in map_data.get("elements", []):
        if element.get("type") != "node":
            continue

        dist = sqrt((element["lat"] - lat) ** 2 + (element["lon"] - lon) ** 2)
        if dist < result_dist:
            result = element
            result_dist = dist

    if result:
        print("Found nearest node ID (on valid highway):", result["id"])
    else:
        print("No valid nearby nodes found.")

    return result


