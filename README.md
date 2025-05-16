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
  ![astar_1](https://github.com/user-attachments/assets/86432fae-02d8-42b2-a4f8-f0b88a697954)

- Dijkstra: Luôn tìm được đường đi ngắn nhất chính xác (trên đồ thị có trọng số không âm) nhưng tính toán nhiều, chạy chậm hơn trên bản đồ lớn.
  ![distra_1](https://github.com/user-attachments/assets/b51c6198-3346-4415-8e3b-24c298450170)

- Greedy Best-First Search: Tìm đường nhanh nhất do chỉ sử dụng thông tin heuristic tham lam; nhược điểm là không đảm bảo tối ưu (có thể bỏ qua đường đi ngắn nhất).
  ![greedy_1](https://github.com/user-attachments/assets/abd27ed1-f774-440b-bd02-56ffc13ae955)

- BFS: Đảm bảo tìm đường ngắn nhất về số bước trên đồ thị không trọng số; nhược điểm tốn bộ nhớ và thời gian xử lý khi không gian tìm kiếm lớn.
  ![bfs_1](https://github.com/user-attachments/assets/b0cbca19-514d-43cd-8fe8-27898f541a12)

- DFS: Thực hiện nhanh nhưng không đảm bảo tìm được đường ngắn nhất, dễ lặp lại và kém hiệu quả trên đồ thị lớn, thời gian tìm được giải pháp rất dài.
  ![dfs_1](https://github.com/user-attachments/assets/72c87bbf-266e-45b7-a739-1dba52c50849)

-------------------------------------------------------
Dữ liệu và thư viện sử dụng
- Dữ liệu bản đồ: Sử dụng bản đồ thực tế từ OpenStreetMap.
- Thư viện hiển thị: Kết quả thuật toán được trực quan hóa trên bản đồ thông qua Pydeck (hỗ trợ hiển thị 3D) và Folium (bản đồ tương tác 2D) trong giao diện Streamlit.
