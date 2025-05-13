# modules/map_renderer.py

import pydeck as pdk
from config import INITIAL_VIEW_STATE, MAP_STYLE_URL

def render_base_map(center_lat=None, center_lon=None, zoom=None, layers=None, app_state=None):
    """Hiển thị bản đồ cơ bản với khả năng zoom/pan, hỗ trợ lấy layers từ app_state nếu cần."""

    # Nếu không truyền vào, dùng mặc định từ config
    lat = center_lat if center_lat is not None else INITIAL_VIEW_STATE["latitude"]
    lon = center_lon if center_lon is not None else INITIAL_VIEW_STATE["longitude"]
    zoom_level = zoom if zoom is not None else INITIAL_VIEW_STATE["zoom"]

    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=zoom_level,
        bearing=INITIAL_VIEW_STATE.get("bearing", 0),
        pitch=INITIAL_VIEW_STATE.get("pitch", 0),
    )

    # Ưu tiên: layers → app_state["layers"] → []
    #used_layers = layers if layers is not None else (app_state.get("layers") if app_state else [])

    # Nếu không có layer cụ thể nào để hiển thị → không render map
    used_layers = layers if layers is not None else (app_state.get("layers") if app_state else [])
    if not used_layers:
        return None  # Chặn việc hiển thị map nếu không có gì để vẽ

    return pdk.Deck(
        map_style=MAP_STYLE_URL,
        initial_view_state=view_state,
        layers=used_layers,
        tooltip={"text": "Bản đồ hiện tại"}
    )

def create_circle_layer(circle_polygon, color=[255, 255, 0, 80]):
    if not circle_polygon or "coordinates" not in circle_polygon or not circle_polygon["coordinates"][0]:
        return None  # Bỏ qua render nếu dữ liệu vòng tròn không hợp lệ
    
    try:
        # Ép kiểu các tọa độ thành float
        coords = [[float(lon), float(lat)] for lon, lat in circle_polygon["coordinates"][0]]
    except (ValueError, TypeError):
        return None  # Bỏ qua nếu không thể ép kiểu
    
    """
    Tạo PolygonLayer để hiển thị hình tròn bán kính.
    """
    return pdk.Layer(
        "PolygonLayer",
        data=[{
            "polygon": circle_polygon["coordinates"][0]
        }],
        get_polygon="polygon",
        get_fill_color=color,
        pickable=False,
        stroked=True,
        get_line_color=[255, 255, 0],
        line_width_min_pixels=1,
    )

def create_node_marker(node, color=[0, 0, 255]):
    if not node or "lon" not in node or "lat" not in node or node["lon"] is None or node["lat"] is None:
        return None  # Bỏ qua render nếu dữ liệu node không hợp lệ
    
    try:
        # Ép kiểu lon và lat thành float
        lon = float(node["lon"])
        lat = float(node["lat"])
    except (ValueError, TypeError):
        return None  # Bỏ qua nếu không thể ép kiểu

    return pdk.Layer(
        "ScatterplotLayer",
        data=[{
            "position": [node["lon"], node["lat"]],
        }],
        get_position="position",
        get_fill_color=color + [255],
        get_radius=100,
        radius_scale=1,
        radius_min_pixels=7,
        radius_max_pixels=20,
        pickable=True
    )

def create_path_layer(path_coords, color=[255, 0, 0], width=1):
    """
    Tạo layer đường đi (visited hoặc shortest path) để hiển thị bằng Pydeck.
    :param path_coords: [[lon, lat], [lon, lat]]
    :param color: [R, G, B]
    :return: pdk.Layer
    """
    return pdk.Layer(
        "PathLayer",
        data=[{
            "path": path_coords,
            "name": "path"
        }],
        get_path="path",
        get_color=color,
        width_scale=3,    # độ rộng đường vẽ
        width_min_pixels=width,    # độ dày của đường vẽ
        pickable=True
    )
