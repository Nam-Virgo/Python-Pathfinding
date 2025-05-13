# modules/folium_picker.py

import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.distance import geodesic
from modules.utils import create_geojson_circle
from modules.osm_service import get_nearest_node, fetch_overpass_data
from modules.graph import build_graph_from_osm

def folium_point_picker(app_state, city_lat,city_lon,radius_km=1.0):
    """
    Hiển thị bản đồ phụ để chọn điểm start và end bằng chuột trái.
    Cập nhật vào app_state: start_node, end_node, circle_polygon, graph
    """
  
    st.markdown(
        """
        <span style="background-color: #e8f0fe; padding: 8px 12px; border-radius: 8px; display: block; margin-bottom: 10px;">
            🖱️ <strong>Nhấn <u>chuột trái</u></strong> để chọn điểm Start/End. Khi đã có cả hai, click sẽ đặt lại Start mới và xoá End.
        </span>
        """,
        unsafe_allow_html=True
    )

    # Vị trí trung tâm mặc định là điểm start hoặc TP.HCM
    if app_state.get("start_node") and "lat" in app_state["start_node"] and "lon" in app_state["start_node"]:
        center = [app_state["start_node"]["lat"], app_state["start_node"]["lon"]]
    else:
        center = [city_lat, city_lon]  # TP.HCM mặc định

    m = folium.Map(location=center, zoom_start=15)

    # Vẽ vùng bán kính nếu có
    if app_state.get("circle_polygon") and "coordinates" in app_state["circle_polygon"] and app_state["circle_polygon"]["coordinates"]:
        folium.Polygon(
            locations=[[lat, lon] for lon, lat in app_state["circle_polygon"]["coordinates"][0]],
            color="orange",
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

    # Vẽ marker nếu có
    if app_state.get("start_node") and "lat" in app_state["start_node"] and "lon" in app_state["start_node"]:
        folium.Marker(
            location=[app_state["start_node"]["lat"], app_state["start_node"]["lon"]],
            icon=folium.Icon(color="blue", icon="play"),
            tooltip="Start"
        ).add_to(m)

    if app_state.get("end_node") and "lat" in app_state["end_node"] and "lon" in app_state["end_node"]:
        folium.Marker(
            location=[app_state["end_node"]["lat"], app_state["end_node"]["lon"]],
            icon=folium.Icon(color="green", icon="flag"),
            tooltip="End"
        ).add_to(m)

    # Hiển thị bản đồ và xử lý click
    data = st_folium(m, width="100%", height=500)

    if data and data.get("last_clicked"):
        lat = data["last_clicked"]["lat"]
        lon = data["last_clicked"]["lng"]
        nearest_node = get_nearest_node(lat, lon)

        # Kiểm tra nearest_node có hợp lệ không trước khi cập nhật app_state
        if nearest_node and "lat" in nearest_node and "lon" in nearest_node and nearest_node["lat"] is not None and nearest_node["lon"] is not None:
            if app_state.get("start_node") and app_state.get("end_node"):
                # Reset khi đã có cả Start và End
                app_state["start_node"] = nearest_node
                app_state["end_node"] = None

                # Vẽ lại vùng bán kính và tạo graph
                circle = create_geojson_circle(nearest_node["lat"], nearest_node["lon"], radius_km)
                app_state["circle_polygon"] = circle

                bbox = circle["coordinates"][0]
                bounding_box = [
                    {"latitude": min(lat for lon, lat in bbox), "longitude": min(lon for lon, lat in bbox)},
                    {"latitude": max(lat for lon, lat in bbox), "longitude": max(lon for lon, lat in bbox)}
                ]
                map_data = fetch_overpass_data(bounding_box)
                app_state["graph"] = build_graph_from_osm(map_data, start_node_id=nearest_node["id"])

            elif not app_state.get("start_node"):
                app_state["start_node"] = nearest_node
                circle = create_geojson_circle(nearest_node["lat"], nearest_node["lon"], radius_km)
                app_state["circle_polygon"] = circle

                bbox = circle["coordinates"][0]
                bounding_box = [
                    {"latitude": min(lat for lon, lat in bbox), "longitude": min(lon for lon, lat in bbox)},
                    {"latitude": max(lat for lon, lat in bbox), "longitude": max(lon for lon, lat in bbox)}
                ]
                map_data = fetch_overpass_data(bounding_box)
                app_state["graph"] = build_graph_from_osm(map_data, start_node_id=nearest_node["id"])

            else:
                # Chọn điểm End
                start = (app_state["start_node"]["lat"], app_state["start_node"]["lon"])
                end = (nearest_node["lat"], nearest_node["lon"])
                if geodesic(start, end).km > radius_km:
                    st.warning(f"⚠️ Điểm End nằm ngoài bán kính {radius_km}km")
                else:
                    app_state["end_node"] = nearest_node
        else:
            st.error("❌ Không tìm thấy node hợp lệ gần vị trí đã chọn.")

    # Nút xác nhận
    confirm_disabled = not (app_state.get("start_node") and app_state.get("end_node"))
    confirmed = st.button("✅ Xác nhận", disabled=confirm_disabled)

    if confirmed:
        # Bổ sung kiểm tra dữ liệu hợp lệ trước khi trả về True
        required_keys = ["start_node", "end_node", "graph"]
        # Kiểm tra thêm xem start_node và end_node có lat/lon hợp lệ không
        if (all(app_state.get(k) for k in required_keys) and 
            "lat" in app_state["start_node"] and "lon" in app_state["start_node"] and
            "lat" in app_state["end_node"] and "lon" in app_state["end_node"]):
            # Ghi kết quả vào file text thay vì in ra giao diện
            with open("output_graph.txt", "w", encoding="utf-8") as f:
                # Ghi thông tin Start Node
                f.write(f"📍 Start Node: {app_state['start_node']}\n")
                
                # Ghi thông tin End Node
                f.write(f"🏁 End Node: {app_state['end_node']}\n")
                
                # Ghi số lượng node trong graph
                f.write(f"🧠 Số lượng node trong graph: {len(app_state['graph'].nodes)}\n\n")
                
                # Ghi danh sách node
                f.write("📋 Danh sách node:\n")
                for node_id, node in app_state["graph"].nodes.items():
                    f.write(f"🔹 ID: {node_id}, Lat: {node.latitude}, Lon: {node.longitude}\n")
                
                # Ghi danh sách cạnh
                f.write("\n🧱 Danh sách cạnh:\n")
                printed_edges = set()
                for node in app_state["graph"].nodes.values():
                    for edge in node.edges:
                        n1 = edge.node1.id
                        n2 = edge.node2.id
                        edge_id = tuple(sorted((n1, n2)))
                        if edge_id not in printed_edges:
                            f.write(f"🔸 Edge giữa Node {n1} ↔ {n2}\n")
                            printed_edges.add(edge_id)

                # Ghi danh sách hàng xóm
                f.write("\n🤝 Danh sách hàng xóm:\n")
                for node in app_state["graph"].nodes.values():
                    neighbor_ids = [n["node"].id for n in node.neighbors]
                    f.write(f"🔹 Node {node.id} có hàng xóm: {neighbor_ids}\n")
                
            # Thông báo cho người dùng rằng dữ liệu đã được ghi vào file
            st.write("✅ Dữ liệu đã được ghi vào file 'output_graph.txt'")
                
            return True
        else:
            st.error("❌ Dữ liệu không hợp lệ. Vui lòng chọn lại.")
            return False

    return False