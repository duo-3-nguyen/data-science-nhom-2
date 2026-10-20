import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/04_eda.ipynb', 'r', encoding='utf-8') as f:
    eda_nb = json.load(f)
with open('notebooks/main.ipynb', 'r', encoding='utf-8') as f:
    main_nb = json.load(f)

def find_cell(nb, query, cell_type=None):
    for i, c in enumerate(nb['cells']):
        if cell_type and c['cell_type'] != cell_type:
            continue
        txt = ''.join(c['source'])
        if query in txt:
            return i, txt
    return -1, ''

queries = [
    ('Diễn giải chi tiết trả lời 4 câu hỏi', 'markdown'),
    ('Nhận xét Họ 4', 'markdown'),
    ('Nhận xét phân tích nhóm Thành phố', 'markdown'),
    ('Nhận xét phân tích nhóm Mùa vụ', 'markdown'),
    ('Nhận xét Hiệu ứng cuối tuần', 'markdown'),
    ('Nhận xét Chu kỳ 24 giờ', 'markdown'),
    ('Nhận xét thận trọng theo năm', 'markdown'),
    ('## 4.3. Năm biểu đồ then chốt', 'markdown'),
    ('chart1_title =', 'code'),
    ('Diễn giải Chart 1', 'markdown'),
    ('chart2_title =', 'code'),
    ('Diễn giải Chart 2', 'markdown'),
    ('chart3_title =', 'code'),
    ('Diễn giải Chart 3', 'markdown'),
    ('chart4_suptitle =', 'code'),
    ('Diễn giải Chart 4', 'markdown'),
    ('chart5_title =', 'code'),
    ('Diễn giải Chart 5', 'markdown'),
    ('## 4.4. Tổng kết & Phát hiện then chốt', 'markdown')
]

all_match = True
for q, ctype in queries:
    ei, etxt = find_cell(eda_nb, q, ctype)
    mi, mtxt = find_cell(main_nb, q, ctype)
    if etxt.strip() != mtxt.strip():
        all_match = False
        print(f'MISMATCH in {q}:')
    else:
        print(f'MATCH: {q}')

if all_match:
    print('\n===> 100% PERFECT MATCH ACROSS ALL 19 EDA SECTIONS AND CHARTS!')
