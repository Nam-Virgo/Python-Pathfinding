# config.py

# URL style bản đồ (sử dụng URL tĩnh đã chọn)
MAP_STYLE_URL = "https://tiles.basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"

# Tọa độ trung tâm mặc định (TP. Hồ Chí Minh)
INITIAL_VIEW_STATE = {
    "latitude": 10.7769,
    "longitude": 106.7009,
    "zoom": 13,
    "pitch": 0,
    "bearing": 0,
}

# Màu sắc mặc định (R, G, B)
INITIAL_COLORS = {
    "start_node_fill": [70, 183, 128],
    "start_node_border": [255, 255, 255],
    "end_node_fill": [152, 4, 12],
    "end_node_border": [0, 0, 0],
    "path": [70, 183, 128],
    "route": [165, 13, 32],
}
