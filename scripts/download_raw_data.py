import kagglehub
import shutil
from pathlib import Path

# Tải dataset
path = Path(kagglehub.dataset_download("rohanrao/air-quality-data-in-india"))

# Thư mục đích
raw_dir = Path("data/raw")
raw_dir.mkdir(parents=True, exist_ok=True)

# Copy toàn bộ file
for file in path.iterdir():
    if file.is_file():
        shutil.copy2(file, raw_dir / file.name)

print("Đã copy dữ liệu vào:", raw_dir.resolve())