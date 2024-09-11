import pandas as pd

def read_csv_with_encoding(file_path, encodings=['utf-8', 'latin1']):
    """
    Đọc file CSV với các mã hóa khác nhau cho đến khi thành công.
    
    :param file_path: Đường dẫn đến file CSV
    :param encodings: Danh sách các mã hóa để thử
    :return: DataFrame chứa dữ liệu từ file CSV
    """
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            print(f"Thử mã hóa '{encoding}' không thành công.")
    raise ValueError("Không thể đọc file CSV với các mã hóa thử.")

def clean_data(df):
    """
    Xử lý và làm sạch dữ liệu trong DataFrame.
    
    :param df: DataFrame chứa dữ liệu gốc
    :return: DataFrame đã được làm sạch
    """
    # Hiển thị thông tin cơ bản
    print("\n\t\t\t\t\t\t\t\t\t\t\t\t===== Dữ liệu gốc =====\n")
    print(df.head())
    print("\n\t===== Thông tin dữ liệu =====\n")
    print(df.info())
    print("\n\t\t\t\t\t\t\t\t\t\t\t\t===== Mô tả dữ liệu =====\n")
    print(df.describe())

    # Xử lý giá trị thiếu
    print("\n==== Số lượng giá trị thiếu ====")
    print(df.isnull().sum())

    # Loại bỏ các hàng có giá trị thiếu
    df_cleaned = df.dropna()

    # Thay thế giá trị thiếu bằng giá trị trung bình (tuỳ chọn)
    # df_cleaned['Tên_Cột'] = df_cleaned['Tên_Cột'].fillna(df_cleaned['Tên_Cột'].mean())

    # Xử lý kiểu dữ liệu nếu cần (tuỳ chọn)
    # df_cleaned['Tên_Cột'] = pd.to_numeric(df_cleaned['Tên_Cột'], errors='coerce')

    # Loại bỏ các cột không cần thiết (tuỳ chọn)
    # df_cleaned = df_cleaned.drop(columns=['Tên_Cột_Thừa'])

    # Chọn các cột cần thiết (tuỳ chọn)
    # df_cleaned = df_cleaned[['Cột_Cần_Thiết_1', 'Cột_Cần_Thiết_2']]

    # Sắp xếp dữ liệu nếu cần (tuỳ chọn)
    # df_cleaned = df_cleaned.sort_values(by='Tên_Cột')

    return df_cleaned

def save_cleaned_data(df, output_path):
    """
    Lưu dữ liệu đã được làm sạch vào file CSV.
    
    :param df: DataFrame chứa dữ liệu đã được làm sạch
    :param output_path: Đường dẫn để lưu file CSV
    """
    df.to_csv(output_path, index=False)
    print("\n===== Dữ liệu đã được xử lý và lưu thành công =====\n")

def main():
    #lưu ý rằng khi bạn đã download Project_AI_IOT_TL-main thì phải thay đổi đường dẫn cho nó và cả đầu ra!
    file_path = r"C:\Users\datzi\Downloads\dữ liệu (FAOSTAT)\Production_Crops_Livestock_E_Americas\Production_Crops_Livestock_E_Americas_NOFLAG.csv"
    output_path = r'D:\python\Thống kê dữ phân tích dự án\data_cleaned.csv'
    
    # Đọc dữ liệu
    data = read_csv_with_encoding(file_path)
    
    # Làm sạch dữ liệu
    data_cleaned = clean_data(data)
    
    # Lưu dữ liệu đã làm sạch
    save_cleaned_data(data_cleaned, output_path)

if __name__ == "__main__":
    main()
