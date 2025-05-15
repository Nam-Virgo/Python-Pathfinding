# Python-Pathfinding
Thuật toán tìm đường trực quan hóa trên bản đồ thực tế
-------------------------------------------------------
Dự án này tập trung xây dựng một giao diện web trực quan bằng Python và Streamlit để minh họa các thuật toán tìm đường trên bản đồ thực tế. Ứng dụng cho phép hiển thị và so sánh kết quả tìm đường của các thuật toán khác nhau trên dữ liệu bản đồ từ OpenStreetMap. Giao diện trực quan giúp người học dễ dàng quan sát hiệu quả và hành vi của từng thuật toán khi tìm đường.

-------------------------------------------------------
Các thuật toán đã triển khai
- A* (A-star)
- Dijkstra
- Greedy Best-First Search
- BFS (Tìm kiếm theo chiều rộng – Breadth-First Search)
- DFS (Tìm kiếm theo chiều sâu – Depth-First Search)

Ưu nhược điểm chính của các thuật toán
- A*: Sử dụng hàm heuristic giúp tìm đường nhanh và chính xác cao; nhược điểm là phụ thuộc vào chất lượng hàm heuristic.
- Dijkstra: Luôn tìm được đường đi ngắn nhất chính xác (trên đồ thị có trọng số không âm) nhưng tính toán nhiều, chạy chậm hơn trên bản đồ lớn.
- Greedy Best-First Search: Tìm đường nhanh nhất do chỉ sử dụng thông tin heuristic tham lam; nhược điểm là không đảm bảo tối ưu (có thể bỏ qua đường đi ngắn nhất).
- BFS: Đảm bảo tìm đường ngắn nhất về số bước trên đồ thị không trọng số; nhược điểm tốn bộ nhớ và thời gian xử lý khi không gian tìm kiếm lớn.
- DFS: Thực hiện nhanh nhưng không đảm bảo tìm được đường ngắn nhất, dễ lặp lại và kém hiệu quả trên đồ thị lớn, thời gian tìm được giải pháp rất dài.

-------------------------------------------------------
Dữ liệu và thư viện sử dụng
- Dữ liệu bản đồ: Sử dụng bản đồ thực tế từ OpenStreetMap.
- Thư viện hiển thị: Kết quả thuật toán được trực quan hóa trên bản đồ thông qua Pydeck (hỗ trợ hiển thị 3D) và Folium (bản đồ tương tác 2D) trong giao diện Streamlit.
