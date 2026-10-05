## Folder

| Folder | Chức năng | Ví dụ |
| --- | --- | --- |
| `data/` | **Dữ liệu** | CSV, JSON, Parquet |
| `data/raw/` | Dữ liệu gốc, chưa sửa | `city_hour.csv` |
| `data/interim/` | Dữ liệu đang xử lý | `cleaned.csv` |
| `data/processed/` | Dữ liệu cuối để phân tích/model | `model_data.csv` |
| `notebooks/` | **Jupyter Notebook** | `01_eda.ipynb` |
| `src/` | Nơi để code thường được được tái sử dụng | `utils.py`, `outliers.py` |
| `scripts/` | **Các script thực hiện tác vụ** | `download_data.py`, `run_pipeline.py` |
| `outputs/` | Kết quả sinh ra | biểu đồ, bảng, model |
| `reports/` | Báo cáo cuối | `report.pdf`, `report.md` |
