import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors

# Đọc file CSV
 #lưu ý rằng khi bạn đã download Project_AI_IOT_TL-main thì phải thay đổi đường dẫn cho nó và cả đầu ra!
file_path = r"C:\Users\datzi\Downloads\dữ liệu (FAOSTAT)\FAOSTAT_data_en_9-10-2024(VN_1990_2022).csv"
data = pd.read_csv(file_path)

# In ra 5 dòng đầu tiên của dữ liệu gốc
print("===== Dữ liệu gốc (5 dòng đầu tiên) =====")
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

# Kiểm tra thông tin của dữ liệu
print("\n===== Thông tin dữ liệu =====")
print(data.info())

# Kiểm tra các năm có trong dữ liệu
print("\n===== Các năm có trong dữ liệu =====")
print(data["Năm"].unique())

# Lọc dữ liệu từ 1990 đến 2022
data_range = data[(data["Năm"] >= 1990) & (data["Năm"] <= 2022)]

# Thêm cột thứ tự (STT) cho dữ liệu đã lọc
data_range.insert(0, "STT", range(1, len(data_range) + 1))

# In ra dữ liệu đã lọc từ năm 1990 đến 2022 dưới dạng bảng
print("\n\t\t\t\t\t\t\t\t\t===== Dữ liệu từ 1990 đến 2022 =====\n")
print(data_range.to_string(index=False, justify="center"))

# Tổng số dòng trong dữ liệu gốc và sau khi lọc
print(f"\nTổng số dòng trong dữ liệu gốc: {len(data)}")
print(f"Tổng số dòng sau khi lọc từ 1990 đến 2022: {len(data_range)}")

# Lọc dữ liệu cho "Area harvested" và "Production"
data_area_harvested = data_range[data_range["Chỉ tiêu"] == "Area harvested"]
total_by_year_area = data_area_harvested.groupby("Năm")["Giá trị"].sum().reset_index()
total_by_year_area["Giá trị (ngàn)"] = total_by_year_area["Giá trị"] / 1000

data_production = data_range[data_range["Chỉ tiêu"] == "Production"]
total_by_year_production = data_production.groupby("Năm")["Giá trị"].sum().reset_index()
total_by_year_production["Giá trị (triệu)"] = (
    total_by_year_production["Giá trị"] / 1000000
)

# Cập nhật font chữ mặc định
plt.rcParams.update({"font.family": "serif", "font.serif": "Times New Roman"})

# Vẽ biểu đồ với hai trục y khác nhau
fig, ax1 = plt.subplots(figsize=(14, 8))

# Vẽ "Area harvested"
sns.lineplot(
    data=total_by_year_area,
    x="Năm",
    y="Giá trị (ngàn)",
    marker="o",
    color="blue",
    linewidth=2,
    markersize=8,
    label="Diện tích thu hoạch (ngàn ha)",
    ax=ax1,
)

# Trục y chính
ax1.set_ylabel("Diện tích thu hoạch (ngàn ha)", color="blue", fontsize=12)
ax1.tick_params(axis="y", labelcolor="blue", labelsize=10)

# Vẽ "Production" trên trục y phụ
ax2 = ax1.twinx()
sns.lineplot(
    data=total_by_year_production,
    x="Năm",
    y="Giá trị (triệu)",
    marker="o",
    color="red",
    linewidth=2,
    markersize=8,
    label="Sản lượng gạo (triệu tấn)",
    ax=ax2,
)

# Trục y phụ
ax2.set_ylabel("Sản lượng gạo (triệu tấn)", color="red", fontsize=12)
ax2.tick_params(axis="y", labelcolor="red", labelsize=10)

# Nhãn trục x
ax1.set_xlabel(
    "Sản Lượng và Diện Tích Thu Hoạch Lúa Gạo Việt Nam (1990 - 2022)", fontsize=14
)

# Thêm lưới
ax1.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

# Thêm chú thích
ax1.legend(loc="upper left", fontsize=10)
ax2.legend(loc="upper right", fontsize=10)

# Tùy chỉnh tooltip với mplcursors
cursor = mplcursors.cursor(hover=True)

# Đảm bảo tất cả các năm từ 1990 đến 2022 đều được hiển thị
years = list(range(1990, 2023, 1))  # Tạo danh sách các năm từ 1990 đến 2022
ax1.set_xticks(years)
ax1.set_xticklabels(
    years, rotation=45, fontsize=10
)  # Đặt các năm này làm nhãn trục x và xoay nhãn nếu cần


# Tùy chỉnh tooltip khi di chuột
@cursor.connect("add")
def on_add(sel):
    # Lấy thông tin từ điểm dữ liệu
    x, y = sel.target
    ax = sel.artist.axes

    # Kiểm tra xem điểm thuộc trục y chính hay phụ
    if ax == ax1:
        # Diện tích thu hoạch
        sel.annotation.set_text(f"Năm: {int(x)}\nDiện tích: {y:.2f} ngàn ha")
        sel.annotation.get_bbox_patch().set_facecolor("blue")
        sel.annotation.get_bbox_patch().set_alpha(0.6)
    else:
        # Sản lượng gạo
        sel.annotation.set_text(f"Năm: {int(x)}\nSản lượng: {y:.2f} triệu tấn")
        sel.annotation.get_bbox_patch().set_facecolor("red")
        sel.annotation.get_bbox_patch().set_alpha(0.6)


# Điều chỉnh bố cục
plt.tight_layout()

# Lưu biểu đồ vào file
#Nhớ khi thay đổi đường dẫn lưu ảnh của bạn vào dự án
output_path = r"D:\python\Thống kê dữ phân tích dự án\file_anh.png" 

print("Đã lưu file ảnh trong dự án !!!")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

# Hiển thị biểu đồ
plt.show()
