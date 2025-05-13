# modules/utils.py

import math

def create_geojson_circle(lat, lon, radius_km=1.0, points=64):
    """
    Tạo polygon hình tròn xung quanh điểm (lat, lon)
    Trả về GeoJSON dạng Polygon
    """
    coords = []
    distance_x = radius_km / (111.320 * math.cos(math.radians(lat)))
    distance_y = radius_km / 110.574

    for i in range(points):
        theta = (i / float(points)) * (2 * math.pi)
        dx = distance_x * math.cos(theta)
        dy = distance_y * math.sin(theta)
        coords.append([lon + dx, lat + dy])

    # Đóng vòng tròn
    coords.append(coords[0])

    return {
        "type": "Polygon",
        "coordinates": [coords]
    }

def get_bounding_box_from_polygon(polygon_coords):
    """
    Nhận vào danh sách toạ độ [lon, lat] của polygon
    Trả về bounding box: [{lat_min, lon_min}, {lat_max, lon_max}]
    """
    lats = [coord[1] for coord in polygon_coords]
    lons = [coord[0] for coord in polygon_coords]

    return [
        {"latitude": min(lats), "longitude": min(lons)},
        {"latitude": max(lats), "longitude": max(lons)}
    ]
