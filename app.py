import streamlit as st
from modules.map_renderer import render_base_map, create_circle_layer, create_node_marker, create_path_layer
from modules.folium_picker import folium_point_picker
import time
from algorithms.pathfinding_algorithm import AStar, Dijkstra, Greedy, BFS, DFS
import pandas as pd

# Màu HEX thành RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

CITY_COORDS = {
    "Hà Nội": [21.0285, 105.8542],
    "TP.Hồ Chí Minh": [10.7769, 106.7009],
    "New York": [40.7128, -74.0060],
    "London": [51.5072, -0.1276],
    "Tokyo": [35.6895, 139.6917],
    "Paris": [48.8566, 2.3522],
    "Singapore": [1.3521, 103.8198],
    "Sydney": [-33.8688, 151.2093],
    "Bangkok": [13.7563, 100.5018],
    "Seoul": [37.5665, 126.9780],
    "Delhi": [28.7041, 77.1025],
    "Moscow": [55.7558, 37.6173],
    "Tokyo (JP)": [35.6895, 139.6917],
    "Shanghai": [31.2304, 121.4737],
    "Hong Kong": [22.3193, 114.1694],
    "Sydney": [-33.8688, 151.2093],
    "Berlin": [52.5200, 13.4050]
}

# ⚙️ Cấu hình trang
st.set_page_config(layout="wide")
st.title("📍 Ứng dụng Tìm Đường Trên Bản Đồ")

# 🧠 Trạng thái phiên
if "show_route_info" not in st.session_state:
    st.session_state["show_route_info"] = False
if "route_history" not in st.session_state:
    st.session_state["route_history"] = []
if "app_state" not in st.session_state:
    st.session_state.app_state = {
        "start_node": None,
        "end_node": None,
        "circle_polygon": None,
        "graph": None
    }
if "selecting_points" not in st.session_state:
    st.session_state.selecting_points = False

# 📦 Sidebar
with st.sidebar:
    st.header("⚙️ Cài đặt thuật toán")
    ALGORITHMS = ["A*", "Dijkstra", "Greedy", "BFS", "DFS"]
    algo_choice = st.selectbox("Chọn thuật toán:", ALGORITHMS)
    start_hex = st.color_picker("🎨 Màu điểm bắt đầu", "#0000ff")
    end_hex = st.color_picker("🎨 Màu điểm kết thúc", "#00ff00")
    radius_km = st.slider("📏 Bán kính tìm kiếm (km)", min_value=1, max_value=5, value=3, step=1)
    speed = st.slider("⏱️ Tốc độ (km/h)", 1, 10, 5, step=1, key="speed_kmh")
    selected_city = st.selectbox("🏙️ Di chuyển đến thành phố", ["-- Không chọn --"] + list(CITY_COORDS.keys()))

    start_color = hex_to_rgb(start_hex)
    end_color = hex_to_rgb(end_hex)
    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button("▶️ Bắt đầu")
    with col2:
        reset_btn = st.button("🔁 Reset")

    if st.button("📊 Xem thông tin đường đi"):
        st.session_state["show_route_info"] = True

    # Reset map
    if reset_btn:
        st.session_state.app_state["start_node"] = None
        st.session_state.app_state["end_node"] = None
        st.session_state.app_state["circle_polygon"] = None
        st.success("✅ Đã reset bản đồ.")

# Lấy tọa độ thành phố
city_lat, city_lon = CITY_COORDS["TP.Hồ Chí Minh"]
if selected_city != "-- Không chọn --":
    city_lat, city_lon = CITY_COORDS[selected_city]

# Chọn điểm
col1, col2 = st.columns([1, 6])
with col1:
    if not st.session_state.selecting_points:
        if st.button("📍 Chọn điểm Start/End"):
            st.session_state.selecting_points = True

if st.session_state.selecting_points:
    confirmed = folium_point_picker(st.session_state.app_state, city_lat, city_lon, radius_km=radius_km)
    if confirmed:
        st.session_state.selecting_points = False
        st.success("✅ Đã chọn xong điểm Start và End")

# Hiển thị bản đồ ban đầu (chưa có đường đi)
layers = []
app_state = st.session_state.app_state

if app_state.get("circle_polygon"):
    circle_layer = create_circle_layer(app_state["circle_polygon"])
    if circle_layer:
        layers.append(circle_layer)
if app_state.get("start_node"):
    layers.append(create_node_marker(app_state["start_node"], color=start_color))
if app_state.get("end_node"):
    layers.append(create_node_marker(app_state["end_node"], color=end_color))

if app_state.get("start_node"):
    center_lat = app_state["start_node"]["lat"]
    center_lon = app_state["start_node"]["lon"]
else:
    center_lat, center_lon = city_lat, city_lon

# Tạo một placeholder map chung
map_placeholder = st.empty()
map_placeholder.pydeck_chart(
    render_base_map(center_lat=center_lat, center_lon=center_lon, layers=layers),
    use_container_width=True
)

with st.expander("🧾 Thông tin đã chọn"):
    st.markdown(f"- **Thuật toán**: `{algo_choice}`")
    st.markdown(f"- **Màu start**: `{start_color}` | **Màu end**: `{end_color}`")
    st.markdown(f"- **Tốc độ**: `{speed}` km/h")
    st.markdown(f"- **Start**: `{app_state.get('start_node')}`")
    st.markdown(f"- **End**: `{app_state.get('end_node')}`")

# 🔄 Xử lý khi nhấn bắt đầu
if start_btn:
    st.info(f"🚀 Đang chạy thuật toán {algo_choice}...")
    graph = app_state.get("graph")
    if not graph:
        st.error("❌ Chưa có đồ thị. Vui lòng chọn điểm Start trước khi chạy.")
    else:
        graph.reset()

        start_node = graph.start_node
        end_node = graph.get_node(app_state["end_node"]["id"])
        if algo_choice == "A*":
            algorithm = AStar()
        elif algo_choice == "Dijkstra":
            algorithm = Dijkstra()
        elif algo_choice == "Greedy":
            algorithm = Greedy()
        elif algo_choice == "BFS":
            algorithm = BFS()
        elif algo_choice == "DFS":
            algorithm = DFS()
        else:
            algorithm = AStar()
        start_time = time.time()
        algorithm.start(start_node, end_node)
        # Sửa: Bỏ tạo placeholder mới (sử dụng placeholder ban đầu)
        
        # Vòng lặp chạy thuật toán và vẽ đường đi đã duyệt (màu xanh)
        while not algorithm.finished:
            algorithm.next_step()
            visited_edges = set()
            for n in graph.nodes.values():
                for e in n.edges:
                    if e.visited:
                        visited_edges.add(e)

            temp_layers = []
            if app_state.get("circle_polygon"):
                temp_layers.append(create_circle_layer(app_state["circle_polygon"]))
            if app_state.get("start_node"):
                temp_layers.append(create_node_marker(app_state["start_node"], color=start_color))
            if app_state.get("end_node"):
                temp_layers.append(create_node_marker(app_state["end_node"], color=end_color))

            for edge in visited_edges:
                temp_layers.append(create_path_layer([
                    [edge.node1.longitude, edge.node1.latitude],
                    [edge.node2.longitude, edge.node2.latitude]
                ], color=[0, 255, 0]))  # màu xanh cho cạnh đã duyệt

            # Cập nhật bản đồ động
            map_placeholder.pydeck_chart(
                render_base_map(
                    center_lat=start_node.latitude,
                    center_lon=start_node.longitude,
                    layers=temp_layers
                ),
                use_container_width=True
            )

            time.sleep(1.0 / st.session_state.speed_kmh)

        end_time = time.time()

        # Đường đi ngắn nhất
        route_nodes = []
        node = end_node
        while node:
            route_nodes.append(node)
            node = node.parent
        route_nodes.reverse()

        route_edges = set()
        for i in range(len(route_nodes) - 1):
            n1, n2 = route_nodes[i], route_nodes[i+1]
            for e in n1.edges:
                if e.get_other_node(n1) == n2:
                    route_edges.add(e)
                    break

        # Xóa các cạnh đã duyệt khỏi visited_edges
        for e in route_edges:
            if e in visited_edges:
                visited_edges.remove(e)

        final_layers = []
        if app_state.get("circle_polygon"):
            final_layers.append(create_circle_layer(app_state["circle_polygon"]))
        if app_state.get("start_node"):
            final_layers.append(create_node_marker(app_state["start_node"], color=start_color))
        if app_state.get("end_node"):
            final_layers.append(create_node_marker(app_state["end_node"], color=end_color))

        for edge in visited_edges:
            final_layers.append(create_path_layer([
                [edge.node1.longitude, edge.node1.latitude],
                [edge.node2.longitude, edge.node2.latitude]
            ], color=[0, 255, 0]))
        for edge in route_edges:
            final_layers.append(create_path_layer([
                [edge.node1.longitude, edge.node1.latitude],
                [edge.node2.longitude, edge.node2.latitude]
            ], color=[255, 0, 0]))

        # Sửa: Vẽ kết quả cuối trên cùng placeholder
        map_placeholder.pydeck_chart(
            render_base_map(
                center_lat=start_node.latitude,
                center_lon=start_node.longitude,
                layers=final_layers
            ),
            use_container_width=True
        )

        # Thêm vào lịch sử
        st.session_state["route_history"].append({
            "Điểm bắt đầu": f"({start_node.latitude:.5f}, {start_node.longitude:.5f})",
            "Điểm kết thúc": f"({end_node.latitude:.5f}, {end_node.longitude:.5f})",
            "Khoảng cách (m)": round(sum(e.weight for e in route_edges) * 1000, 2),
            "Thuật toán": algo_choice,
            "Thời gian (s)": round(end_time - start_time, 4)
        })

if st.session_state.get("show_route_info") and st.session_state.get("route_history"):
    st.markdown("## 📋 Thông tin đường đi đã tìm")
    df = pd.DataFrame(st.session_state["route_history"])
    st.dataframe(df)
