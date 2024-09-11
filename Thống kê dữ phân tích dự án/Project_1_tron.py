import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Đọc file CSV
file_path = r"C:\Users\datzi\Downloads\dữ liệu (FAOSTAT)\FAOSTAT_data_en_9-10-2024(Thị phần sản xuất lúa gạo theo khu vực).csv"
data = pd.read_csv(file_path)

print("===== Dữ liệu gốc (!!!!!) =====")
print(data.head())

# Đổi tên cột
column_mapping = {
    "Domain Code": "Mã lĩnh vực",
    "Domain": "Lĩnh vực",
    "Area Code": "Mã vùng",
    "Area": "Vùng",
    "Element Code": "Mã chỉ tiêu",
    "Element": "Chỉ tiêu",
    "Item Code": "Mã mục",
    "Item": "Mục",
    "Year Code": "Mã năm",
    "Year": "Năm",
    "Unit": "Đơn vị",
    "Value": "Giá trị",
    "Flag": "Cờ",
    "Flag Description": "Mô tả cờ",
    "Note": "Ghi chú",
}
data.rename(columns=column_mapping, inplace=True)

# Thêm cột số thứ tự
data.insert(0, "STT", range(1, len(data) + 1))

# Kiểm tra cột 'Năm'
if "Năm" in data.columns:
    data_filtered = data[data["Năm"] >= 2000]
else:
    # Nếu không có cột 'Năm', làm việc với dữ liệu hiện có
    data_filtered = data

# In ra dữ liệu đã lọc từ năm 2000 trở đi dưới dạng bảng
print("\n\t\t\t\t\t\t\t\t\t===== Dữ liệu từ 2000 đến 2022 =====\n")
print(data_filtered.to_string(index=False, justify="center"))

# Tổng số dòng trong dữ liệu gốc và sau khi lọc
print(f"\nTổng số dòng trong dữ liệu gốc: {len(data)}")
print(f"Tổng số dòng sau khi lọc từ 2000 đến 2022: {len(data_filtered)}")

# Nhóm dữ liệu theo vùng và tính tổng giá trị
data_grouped = data_filtered.groupby("Vùng")["Giá trị"].sum().reset_index()

# Định nghĩa danh sách màu
colors = ["#66b3ff", "#00ff00", "#ffff00", "#ff0000", "#c2c2f0", "#ffb3e6"]

# Vẽ đồ thị hình tròn
fig, ax = plt.subplots(figsize=(12, 8))
wedges, texts, autotexts = ax.pie(
    data_grouped["Giá trị"],
    labels=data_grouped["Vùng"],  # Thêm nhãn cho các phần
    colors=colors,  # Sử dụng danh sách màu tùy chỉnh
    startangle=140,
    wedgeprops=dict(width=1),  # Đặt độ dày của các phần để không có khoảng trống
    autopct=lambda p: "",  # Xóa các phần trăm bên trong biểu đồ
)

# Xóa nhãn chú thích bên trong biểu đồ
for text in texts:
    text.set_text("")

# Tạo đối tượng FontProperties để thay đổi font chữ
font_properties = FontProperties(
    family="serif", fname="C:/Windows/Fonts/times.ttf"
)  # Đường dẫn đến font Times New Roman

# Thay đổi font chữ của tiêu đề
plt.title(
    "Thị Phần Sản Xuất Lúa Gạo Theo Khu Vực Trung Bình (1994 - 2022)",
    fontdict={"fontsize": 14, "fontweight": "bold", "fontname": "Times New Roman"},
)

# Thay đổi font chữ cho các nhãn
plt.setp(texts, family="serif", fontname="Times New Roman")

# Thêm chú thích bên ngoài biểu đồ với font Times New Roman
plt.legend(
    wedges,
    data_grouped["Vùng"],  # Sử dụng nhãn của các phần
    title="Khu vực",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),  # Đặt chú thích ở bên ngoài biểu đồ
    fontsize="small",
    title_fontsize="13",
    prop=font_properties,  # Áp dụng thuộc tính font chữ cho chú thích
)

plt.axis("equal")  # Đảm bảo hình tròn không bị méo

# Tạo đối tượng Annotation để hiển thị thông tin và mũi tên
info_box = ax.annotate(
    "",
    xy=(0, 0),
    xytext=(0.1, 0.1),
    textcoords="axes fraction",
    bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"),
    fontsize=12,
    family="serif",
    fontname="Times New Roman",
    arrowprops=dict(arrowstyle="->", color="black"),  # Mũi tên chỉ vào hộp thông báo
)
info_box.set_visible(False)  # Ẩn thông báo ban đầu


# Tạo hiệu ứng bóng khi di chuột vào các phần
def on_hover(event):
    found = False
    for wedge in wedges:
        if wedge.contains(event)[0]:
            index = wedges.index(wedge)
            label = data_grouped["Vùng"].iloc[index]
            value = data_grouped["Giá trị"].iloc[index]
            info_box.set_text(f"{label}: {value:,.0f}")
            info_box.xy = event.xdata, event.ydata
            info_box.set_visible(True)

            # Thay đổi màu sắc và kích thước của phần khi di chuột
            wedge.set_edgecolor(
                "orange"
            )  # Tạo hiệu ứng sáng bóng bằng cách đổi màu viền
            wedge.set_linewidth(3)  # Tăng kích thước viền để làm nổi bật
            plt.draw()
            found = True
            break
    if not found:
        info_box.set_visible(False)
        # Đặt lại màu sắc và kích thước của các phần khi không di chuột
        for wedge in wedges:
            wedge.set_edgecolor("none")
            wedge.set_linewidth(0)
        plt.draw()


# Kích hoạt sự kiện di chuột
fig.canvas.mpl_connect("motion_notify_event", on_hover)

# Lưu biểu đồ vào file
#Nhớ khi thay đổi đường dẫn lưu ảnh của bạn vào dự án
output_path = r"D:\python\Thống kê dữ phân tích dự án\file_anh_bieu_do_tron.png"
print("Đã lưu file ảnh trong dự án !!!")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

plt.show()
