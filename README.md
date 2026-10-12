# 1. Cấu trúc

## 1.1 Cấu trúc folder

| Folder | Chức năng | Ví dụ |
| --- | --- | --- |
| `data/` | **Dữ liệu** | CSV, JSON, Parquet |
| `data/raw/` | Dữ liệu gốc, chưa sửa | `city_hour.csv` |
| `data/processed/` | Dữ liệu cuối để phân tích/model | `model_data.csv` |
| `notebooks/` | **Jupyter Notebook** | `01_eda.ipynb` |
| `scripts/` | **Các script thực hiện tác vụ** | `download_data.py`, `run_pipeline.py` |
| `reports/` | Báo cáo cuối | `report.pdf`, `report.md` |


# 2. Cài đặt

## 2.1. Cài thư viện
```cmd
pip install -r requirements.txt
```

## 2.2. Tải thư data raw
```
python scripts\download_raw_data.py
```