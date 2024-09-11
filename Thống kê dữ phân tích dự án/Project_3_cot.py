import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.lines import Line2D
import mplcursors

# Đọc file CSV
 #lưu ý rằng khi bạn đã download Project_AI_IOT_TL-main thì phải thay đổi đường dẫn cho nó và cả đầu ra!
file_path = r"C:\Users\datzi\Downloads\dữ liệu (FAOSTAT)\FAOSTAT_data_en_9-10-2024(Hàng hóa được sản xuất nhiều nhất, Thế giới + (thế giới)).csv"
data = pd.read_csv(file_path)

# In ra 5 dòng đầu tiên của dữ liệu gốc
print("===== Dữ liệu gốc (5 dòng đầu tiên) =====")
print(data.head())

# Kiểm tra danh sách các cột
print("\n===== Danh sách các cột =====")
print(data.columns)

# Kiểm tra giá trị trong cột 'Item'
print("\n===== Giá trị trong cột 'Item' =====")
print(data["Item"].unique())

# Ví dụ: Lọc dữ liệu cho tất cả các mặt hàng (items)
data_filtered = data[["Item", "Value"]]

print("\n===== Dữ liệu đã lọc =====")
print(data_filtered.head())
print("\n===== Thông tin dữ liệu đã lọc =====")
print(data_filtered.info())
print("\n===== Giá trị trong cột 'Value' =====")
print(data_filtered["Value"].head())

# Thêm cột thứ tự (STT) cho dữ liệu đã lọc
data_filtered.insert(0, "STT", range(1, len(data_filtered) + 1))

# Xử lý giá trị thiếu trong cột 'Value'
data_filtered = data_filtered.dropna(subset=["Value"])
data_filtered["Value"] = pd.to_numeric(data_filtered["Value"], errors="coerce")

# Nhóm dữ liệu theo mặt hàng và tính tổng giá trị
data_grouped = data_filtered.groupby("Item").agg({"Value": "sum"}).reset_index()

# Sắp xếp dữ liệu theo giá trị giảm dần để dễ đọc
data_grouped = data_grouped.sort_values(by="Value", ascending=False)

# Thêm cột thứ tự (STT) cho dữ liệu đã nhóm
data_grouped.insert(0, "STT", range(1, len(data_grouped) + 1))

# Cấu hình hiển thị pandas để in đầy đủ dữ liệu
pd.set_option("display.max_columns", None)  # Hiển thị tất cả các cột
pd.set_option(
    "display.max_rows", None
)  # Hiển thị tất cả các hàng (cẩn thận với dữ liệu lớn)
pd.set_option("display.max_colwidth", None)  # Hiển thị đầy đủ nội dung cột

# In ra dữ liệu đã nhóm dưới dạng bảng
print("\n===== Dữ liệu đã nhóm =====")
print(data_grouped.to_string(index=False, justify="center"))

# Vẽ biểu đồ cột với chú thích màu sắc
plt.figure(figsize=(12, 8))
colors = plt.cm.viridis_r(range(len(data_grouped)))  # Chọn màu sắc từ bảng màu có sẵn
bars = plt.bar(
    data_grouped["Item"], data_grouped["Value"], color=colors, edgecolor="black"
)  # Thêm viền đen cho các cột
plt.xlabel("Mặt hàng", fontsize=12, fontname="Times New Roman")
plt.ylabel("Tổng giá trị", fontsize=12, fontname="Times New Roman")
plt.title(
    "Biểu đồ cột tổng giá trị của các mặt hàng", fontsize=14, fontname="Times New Roman"
)
plt.xticks(
    rotation=45, ha="right", fontsize=10, fontname="Times New Roman"
)  # Xoay nhãn trục x theo hướng chéo

# Đặt định dạng trục Y để không hiển thị dạng số lũy thừa
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

# Thêm lưới vào biểu đồ
plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

# Tạo chú thích màu sắc với hình tròn nhỏ
production_color = colors[0]  # Chọn màu của cột đầu tiên hoặc màu bạn muốn
legend_elements = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label="Production",
        markersize=10,
        markerfacecolor=production_color,
    )
]
plt.legend(
    handles=legend_elements,
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
    prop={"family": "Times New Roman", "size": 12},
)

# Sử dụng mplcursors để hiển thị thông tin khi di chuyển chuột
cursor = mplcursors.cursor(bars, hover=True)
cursor.connect(
    "add",
    lambda sel: sel.annotation.set_text(
        f'{data_grouped["Item"].iloc[sel.index]}\nValue: {data_grouped["Value"].iloc[sel.index]:,.0f}'
    ),
)
cursor.connect(
    "remove", lambda sel: sel.annotation.set_visible(False)
)  # Ẩn chú thích khi không hover

plt.tight_layout()

# Lưu biểu đồ vào file

#Nhớ khi thay đổi đường dẫn lưu ảnh của bạn vào dự án
output_path = r"D:\python\Thống kê dữ phân tích dự án\file_anh_bieu_do_cot.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print("Đã lưu file ảnh trong dự án !!!")

plt.show()

# Tổng số dòng trong dữ liệu gốc và sau khi nhóm
print(f"\nTổng số dòng trong dữ liệu gốc: {len(data)}")
print(f"Tổng số dòng sau khi nhóm: {len(data_grouped)}")
