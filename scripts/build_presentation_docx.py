import sys
import shutil
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

# Colors
COLOR_PRIMARY = RGBColor(27, 54, 93)      # Navy Deep #1B365D
COLOR_SECONDARY = RGBColor(41, 128, 185)  # Soft Blue #2980B9
COLOR_ACCENT = RGBColor(192, 57, 43)      # Brick Red #C0392B
COLOR_DARK = RGBColor(44, 62, 80)         # Charcoal Dark #2C3E50
COLOR_MUTED = RGBColor(127, 140, 141)     # Muted Gray #7F8C8D
COLOR_STAGE = RGBColor(142, 68, 173)      # Purple for Stage Directions #8E44AD
COLOR_SPEECH = RGBColor(20, 40, 65)       # Spoken text

def set_cell_background(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=200, right=200):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tc_pr.append(tc_mar)

def add_callout(doc, text_content, title="LỜI THOẠI MẪU (NÓI TRỰC TIẾP TRƯỚC LỚP)", box_type="speech"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    
    if box_type == "speech":
        border_hex = "2980B9" # Blue
        bg_hex = "F4F9FD"
        badge_color = RGBColor(41, 128, 185)
    elif box_type == "stage":
        border_hex = "8E44AD" # Purple
        bg_hex = "FBF6FD"
        badge_color = RGBColor(142, 68, 173)
    elif box_type == "qa":
        border_hex = "27AE60" # Green
        bg_hex = "F4FDF7"
        badge_color = RGBColor(39, 174, 96)
    else: # tip / warning
        border_hex = "E67E22" # Orange
        bg_hex = "FEF9F3"
        badge_color = RGBColor(230, 126, 34)

    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=140, bottom=140, left=220, right=200)
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_hex}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"★ {title}\n")
    run_t.bold = True
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = badge_color
    
    run_body = p.add_run(text_content)
    run_body.font.size = Pt(10.5)
    run_body.font.color.rgb = COLOR_SPEECH
    run_body.font.name = 'Calibri'
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(11.5)
    r.bold = True
    r.font.color.rgb = COLOR_DARK
    return h

def add_para(doc, text, bold_prefix="", space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_DARK
        r_pre.font.name = 'Calibri'
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_DARK
    return p

def add_stage_cue(doc, cue_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"👉 [HÀNH ĐỘNG / ĐIỀU KHIỂN SLIDE]: {cue_text}")
    r.font.name = 'Calibri'
    r.font.size = Pt(9.5)
    r.italic = True
    r.bold = True
    r.font.color.rgb = COLOR_STAGE
    return p

doc = docx.Document()

# Set standard margins (1 inch)
for sec in doc.sections:
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.8)
    sec.right_margin = Inches(0.8)

# ----------------- COVER / HEADER -----------------
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(10)
title_p.paragraph_format.space_after = Pt(4)
title_run = title_p.add_run("KỊCH BẢN THUYẾT TRÌNH CHI TIẾT - PHẦN 4: EDA")
title_run.font.name = 'Calibri'
title_run.font.size = Pt(22)
title_run.bold = True
title_run.font.color.rgb = COLOR_PRIMARY

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(12)
sub_run = sub_p.add_run("Dành cho Sinh viên năm 2 | Chuẩn hóa theo biểu đồ thực tế 100% | Tự nhiên, tự tin, mạch lạc")
sub_run.font.name = 'Calibri'
sub_run.font.size = Pt(12)
sub_run.italic = True
sub_run.font.color.rgb = COLOR_SECONDARY

# Overview box
intro_overview = (
    "• Đề tài: Phân tích Khám phá Dữ liệu Chất lượng Không khí Ấn Độ (Air Quality Dataset - CPCB).\n"
    "• Định vị phong cách: Nói tự nhiên, dễ hiểu, tránh thuật ngữ hàn lâm trừu tượng, bám sát con số trên biểu đồ.\n"
    "• Cấu trúc phần 4 gồm 3 trụ cột lớn:\n"
    "   1. Mục 4.1: Bốn họ số đo thống kê mô tả (Slide 16 INFO3020) - 'Bản chụp X-quang' toàn cảnh dữ liệu.\n"
    "   2. Mục 4.2: Phân tích theo nhóm chuyên sâu (Thành phố, Mùa vụ, Cuối tuần vs Ngày thường, 24 giờ, Xu hướng năm).\n"
    "   3. Mục 4.3: Năm biểu đồ then chốt (5 Headline Charts) - Trọng tâm ghi điểm cao nhất của bài báo cáo.\n"
    "   4. Mục 4.4: 5 Phát hiện then chốt & Khuyến nghị thực tiễn."
)
add_callout(doc, intro_overview, title="TỔNG QUAN BÀI THUYẾT TRÌNH PHẦN 4", box_type="tip")

# ----------------- SECTION 0: HƯỚNG DẪN TÂM THẾ -----------------
add_heading_1(doc, "0. BÍ QUYẾT TỎA SÁNG KHI THUYẾT TRÌNH CHO SINH VIÊN NĂM 2")
add_para(doc, "Nhiều bạn sinh viên năm 2 khi thuyết trình môn Data Science thường mắc 2 lỗi: Một là đọc lại y nguyên code hoặc slide; Hai là cố nhét các từ ngữ quá học thuật (như 'phân bố leptokurtic', 'hệ số bất đối xứng dương đa biến'...) khiến thầy cô cảm thấy bài bị gượng gạo, còn bạn bè bên dưới thì 'ngủ gật'.")
add_para(doc, "Để đạt điểm A trong mắt giảng viên, bạn chỉ cần nhớ 3 nguyên tắc vàng sau:")
add_para(doc, "1. Nói bằng ngôn ngữ trực quan: Hãy biến con số thành hình ảnh đời thực. Ví dụ thay vì nói 'hệ số Skewness dương lớn', hãy nói 'dữ liệu bị kéo lệch mạnh vì những ngày ô nhiễm đột biến kinh hoàng vào mùa đông'.", bold_prefix="• ")
add_para(doc, "2. Nói đúng những gì mắt người nghe đang nhìn thấy trên slide: Tuyệt đối không để slide chiếu một đằng, miệng nói một nẻo. Khi slide hiện Boxplot có Ahmedabad ở đỉnh, bạn phải nhắc đến Ahmedabad đầu tiên chứ không được bỏ quên.", bold_prefix="• ")
add_para(doc, "3. Luôn chỉ ra câu chuyện (Insight) và bài học thực tiễn: Thầy cô không chỉ chấm bạn 'vẽ được biểu đồ', mà chấm ở việc bạn 'hiểu biểu đồ đó nói lên điều gì cho sức khỏe con người và xã hội'.", bold_prefix="• ")

# ----------------- SECTION 1: LỜI MỞ ĐẦU -----------------
add_heading_1(doc, "1. LỜI MỞ ĐẦU: CHUYỂN TIẾP TỪ TIỀN XỬ LÝ SANG EDA (~1 PHÚT)")
add_stage_cue(doc, "Đứng thẳng, mắt nhìn bao quát cả lớp và thầy cô, mỉm cười tự tin, bấm slide sang trang bìa Phần 4.")

speech_open = (
    "\"Kính thưa thầy/cô và các bạn trong lớp,\n\n"
    "Ở phần trước, bạn [Tên bạn nhóm viên] đã trình bày rất chi tiết về cách nhóm em 'dọn rác' dữ liệu — từ việc "
    "xử lý các giá trị trần, khử các chuỗi số 0 lỗi cảm biến, cho đến nội suy và tính toán lại chỉ số AQI chuẩn xác cho "
    "hơn 2.5 triệu dòng quan trắc thô.\n\n"
    "Sau khi dữ liệu đã hoàn toàn sạch sẽ, nhóm em tổng hợp lại thành 2 bảng cấp độ thành phố: bảng city_hour với hơn 707 nghìn dòng "
    "để theo dõi từng giờ, và bảng city_day với hơn 29.5 nghìn dòng để theo dõi từng ngày của 26 thành phố lớn tại Ấn Độ.\n\n"
    "Và bây giờ, câu hỏi quan trọng nhất được đặt ra là: 'Đằng sau những con số khổng lồ đó, bức tranh ô nhiễm thực tế ở Ấn Độ "
    "đang diễn ra như thế nào? Nơi nào người dân phải chịu đựng không khí độc hại nhất, mùa nào là đỉnh điểm, và tại sao lại như vậy?'\n\n"
    "Sau đây, em xin phép đại diện nhóm trình bày Phần 4: Phân tích Khám phá Dữ liệu (EDA). Nhóm em xây dựng phần này dựa trên "
    "đúng 4 họ số đo thống kê mô tả chuẩn trong Slide bài giảng và 5 biểu đồ then chốt để trả lời trọn vẹn những câu hỏi trên!\""
)
add_callout(doc, speech_open, title="LỜI THOẠI MẪU: MỞ ĐẦU & BẮT NHỊP", box_type="speech")

# ----------------- SECTION 2: MỤC 4.1 BỐN HỌ SỐ ĐO -----------------
add_heading_1(doc, "2. MỤC 4.1: BỐN HỌ SỐ ĐO THỐNG KÊ MÔ TẢ (SLIDE 16) (~2.5 PHÚT)")
add_para(doc, "Mục tiêu: Chứng minh cho giảng viên thấy nhóm nắm rất chắc lý thuyết thống kê mô tả (Block 2 - Slide 16) bằng cách trả lời trọn vẹn 4 câu hỏi cốt lõi.")
add_stage_cue(doc, "Chuyển sang slide bảng tổng hợp 4 họ số đo hoặc hình biểu đồ supp_correlation_shape.png.")

speech_41 = (
    "\"Kính thưa thầy cô, thay vì chỉ tính toán trung bình một cách qua loa, nhóm em đã áp dụng trọn vẹn 'Bốn họ số đo thống kê mô tả' "
    "theo đúng Slide 16 của môn học, giống như một bản chụp X-quang 4 chiều cho toàn bộ tập dữ liệu:\n\n"
    "1. Họ thứ nhất là Location — trả lời câu hỏi: 'Mức độ điển hình ở đây là bao nhiêu?'\n"
    "Nếu nhìn vào bụi mịn PM2.5, mức trung vị (Median) của toàn bộ các thành phố là 48.4 µg/m³. Con số này đã tiệm cận mức trần 60 µg/m³ "
    "trong quy chuẩn 24 giờ của Ấn Độ và cao gấp hơn 3.2 lần ngưỡng an toàn khuyến nghị của Tổ chức Y tế Thế giới (WHO là 15 µg/m³). "
    "Chỉ số AQI trung vị là 115.3, tức là nằm ở mức Moderate (Vừa phải). Tuy nhiên, giá trị trung bình (Mean) của AQI lại vọt lên tận 161.9. "
    "Tại sao lại có sự lệch nhau lớn như vậy giữa Mean và Median? Đó chính là câu trả lời của họ số đo tiếp theo.\n\n"
    "2. Họ thứ hai là Spread — trả lời câu hỏi: 'Dữ liệu phân tán hay ổn định?'\n"
    "Câu trả lời là: Không khí ở Ấn Độ cực kỳ bất ổn và biến động dữ dội! Khoảng tứ phân vị IQR của AQI lên tới 119.1 và hệ số biến thiên CV đạt 78%. "
    "Đặc biệt nhất là khí CO, hệ số biến thiên lên tới 253% (CV = 2.53), cho thấy có những ngày nồng độ khí độc phát thải đột biến gấp hàng chục lần ngày thường.\n\n"
    "3. Họ thứ ba là Shape — trả lời câu hỏi then chốt: 'Hình dạng phân bố thế nào và thước đo nào là hợp lệ ở đây?'\n"
    "Nhìn vào biểu đồ phân bố tích lũy ECDF, tất cả các chất đều có hệ số lệch phải Skewness dương rất lớn (>1.0), đặc biệt là CO đạt 7.5 và AQI đạt 2.8. "
    "Hệ số nhọn Kurtosis cao vút (AQI là 16.0 và CO lên tới 82.4), minh chứng cho phân bố đuôi rất dày (heavy-tailed).\n"
    "-> VÀ ĐÂY LÀ ĐIỂM MẤU CHỐT NHẤT: Vì dữ liệu bị kéo lệch rất mạnh về bên phải bởi các đợt ô nhiễm cực đoan mùa đông, nên nếu chúng ta dùng "
    "giá trị Trung bình (Mean) và Độ lệch chuẩn (Std), chúng ta sẽ bị các giá trị ngoại lai đánh lừa! Do đó, nhóm em khẳng định: "
    "Số Trung vị (Median) và Khoảng tứ phân vị (IQR) mới là những thước đo trung thực, chuẩn xác và có giá trị khoa học nhất để đại diện cho chất lượng không khí!\n\n"
    "4. Họ thứ tư là Relationship — trả lời câu hỏi: 'Chất nào đi cùng với chất nào?'\n"
    "Qua ma trận tương quan Spearman, nhóm em rút ra 3 phát hiện cực kỳ thú vị:\n"
    "- Thứ nhất: Bụi mịn chính là 'kẻ cầm đầu' chi phối toàn bộ chỉ số ô nhiễm. AQI có tương quan mạnh nhất với PM10 (hệ số r = 0.88) và PM2.5 (r = 0.84).\n"
    "- Thứ hai: Các khí thải giao thông và công nghiệp luôn đi kèm với nhau, như PM2.5 và PM10 tương quan rất cao (r = 0.88), NO2 và NOx đạt 0.69.\n"
    "- Và thứ ba: Riêng khí Ozone (O3) lại có xu hướng ngược pha với NO (r = -0.05). Lý do hóa học là vì khí NO phát thải từ ống xả xe cộ phản ứng trực tiếp "
    "tiêu thụ phân tử Ozone ở sát mặt đất!\""
)
add_callout(doc, speech_41, title="LỜI THOẠI MẪU: MỤC 4.1 BỐN HỌ SỐ ĐO", box_type="speech")

# ----------------- SECTION 3: MỤC 4.2 PHÂN TÍCH NHÓM -----------------
add_heading_1(doc, "3. MỤC 4.2: PHÂN TÍCH THEO NHÓM CHUYÊN SÂU (~3 PHÚT)")
add_para(doc, "Mục tiêu: Thể hiện độ sâu của bài làm (Depth of EDA - Rubric 25%) bằng cách phân tích bóc tách theo 5 lát cắt: Địa lý thành phố, Mùa vụ, Ngày thường vs Cuối tuần, Chu kỳ 24h, và Diễn biến theo năm.")

add_heading_2(doc, "3.1. Nhóm Thành phố & Địa lý: Khoảng cách Bắc - Nam vời vợi")
add_stage_cue(doc, "Chỉ vào slide so sánh Top 5 và Bottom 5 thành phố.")
speech_421 = (
    "\"Bây giờ, nếu bóc tách dữ liệu theo từng nhóm thành phố, chúng ta sẽ thấy một sự phân hóa địa lý gây sốc:\n"
    "- Đứng đầu bảng ô nhiễm không thể không nhắc tới Ahmedabad — thành phố công nghiệp ở miền Tây với AQI trung bình lên tới 398.8 "
    "và trung vị là 350.8! Kế tiếp là một loạt các đại đô thị vùng đồng bằng sông Hằng ở phía Bắc như Delhi (AQI trung vị 236.9), "
    "Gurugram (203.8), Lucknow (191.6) và Patna (167.8). Toàn bộ nhóm này đều có chỉ số AQI vượt ngưỡng Poor (Kém) cho đến Very Poor.\n"
    "- Ngược lại hoàn toàn, ở nhóm cuối bảng, các đô thị vùng đồi núi Đông Bắc và ven biển Nam Ấn lại có bầu không khí cực kỳ trong lành: "
    "Aizawl có AQI trung vị chỉ 27.0 (chuẩn Good), Shillong là 46.4, Thiruvananthapuram là 66.1, Coimbatore là 73.5.\n"
    "-> Nghĩa là, mức độ ô nhiễm giữa thành phố ô nhiễm nhất và sạch nhất tại Ấn Độ chênh lệch nhau tới hơn 13 lần! "
    "Ngay cả các siêu đô thị ven biển như Mumbai (AQI 90.4) hay Chennai (97.2), dù xe cộ đông đúc nhưng nhờ gió biển thổi liên tục giúp "
    "khuếch tán chất ô nhiễm, nên AQI vẫn thấp hơn Delhi tới hơn 2.5 lần!\""
)
add_callout(doc, speech_421, title="LỜI THOẠI MẪU: NHÓM THÀNH PHỐ", box_type="speech")

add_heading_2(doc, "3.2. Nhóm Mùa vụ & Tỷ lệ Mùa Đông / Mùa Mưa")
add_stage_cue(doc, "Chỉ vào biểu đồ cột thể hiện tỷ lệ Winter / Monsoon của Top 8 thành phố.")
speech_422 = (
    "\"Lát cắt thứ hai là về Mùa vụ khí tượng:\n"
    "Chất lượng không khí Ấn Độ thay đổi theo mùa một cách chóng mặt:\n"
    "- Mùa đông (tháng 12 đến tháng 2) là 'cơn ác mộng': AQI trung vị toàn quốc lên tới 172.8 (trung bình là 220.8), PM2.5 trung vị 74.0 µg/m³, "
    "và có tới 42.4% số ngày rơi vào mức ô nhiễm Kém (Poor) trở lên.\n"
    "- Trong khi đó, Mùa mưa gió mùa (Monsoon, tháng 6 đến tháng 9) là 'vị cứu tinh': AQI trung vị giảm sâu xuống chỉ còn 90.4, "
    "PM2.5 chỉ còn 33.1 µg/m³, và tỷ lệ ngày Poor giảm chỉ còn 9.0% nhờ những trận mưa lớn gột rửa bầu không khí.\n"
    "- ĐẶC BIỆT NHẤT TRÊN BIỂU ĐỒ NÀY: Khi so sánh chỉ số giữa Mùa đông so với Mùa mưa, đứng đầu không phải là Delhi, mà là Guwahati! "
    "Tại Guwahati, AQI mùa đông vọt lên gấp 6.17 lần mùa mưa (từ 46.3 nhảy vọt lên 285.4)! Kế tiếp là Kolkata gấp 4.34 lần, "
    "Patna gấp 3.77 lần, Lucknow gấp 3.28 lần và Delhi gấp 2.37 lần.\n"
    "Cơ chế khoa học đằng sau hiện tượng này là vào mùa đông, lớp không khí lạnh sát mặt đất bị một lớp khí ấm bên trên đè nén, "
    "tạo thành một chiếc 'nắp nồi' nhiệt quyển (inversion layer), nhốt chặt toàn bộ khói bụi sinh hoạt và giao thông lại, "
    "không cho thoát lên tầng cao!\""
)
add_callout(doc, speech_422, title="LỜI THOẠI MẪU: MÙA VỤ & TỶ LỆ WINTER / MONSOON", box_type="speech")

add_heading_2(doc, "3.3. Nhóm Ngày thường vs Cuối tuần (Hiệu ứng cuối tuần)")
add_stage_cue(doc, "Nhìn về phía các bạn trong lớp với nụ cười dí dỏm, đặt một câu hỏi tương tác nhỏ.")
speech_423 = (
    "\"Chắc hẳn nhiều bạn ở đây sẽ nghĩ: 'Vào cuối tuần, người dân nghỉ làm, ít xe cộ đi lại hơn thì không khí chắc chắn sẽ sạch hơn nhiều đúng không?'\n"
    "Nhưng khi nhóm em chạy số liệu đối chiếu giữa Weekday (thứ 2 đến thứ 6) và Weekend (thứ 7, Chủ nhật), kết quả thu được lại gây bất ngờ lớn: "
    "Chỉ số nồng độ giữa ngày thường và cuối tuần gần như... y hệt nhau!\n"
    "- PM2.5 trung vị ngày thường là 48.49 µg/m³, cuối tuần là 48.21 µg/m³ (chênh lệch chưa tới 0.6%).\n"
    "- AQI trung vị ngày thường là 115.11, cuối tuần là 115.62 (thậm chí cuối tuần còn hơi nhỉnh hơn một chút!).\n"
    "Tại sao lại như vậy? Nhóm em đã tìm hiểu sâu bối cảnh và rút ra 2 nguyên nhân cốt lõi:\n"
    "1. Các nguồn phát thải nền khổng lồ ở Ấn Độ như các nhà máy nhiệt điện đốt than liên vùng, việc đốt than/củi đun nấu gia đình, "
    "và các xe tải hạng nặng chở hàng xuyên bang vẫn hoạt động miệt mài 24/7 không có ngày nghỉ.\n"
    "2. Hạt bụi mịn PM2.5 có kích thước siêu nhỏ, có thể lơ lửng trong bầu khí quyển nhiều ngày đến cả tuần, "
    "chứ không thể tự động biến mất chỉ sau 1–2 ngày nghỉ cuối tuần!\""
)
add_callout(doc, speech_423, title="LỜI THOẠI MẪU: NGÀY THƯỜNG VS CUỐI TUẦN", box_type="speech")

# ----------------- SECTION 4: 5 HEADLINE CHARTS -----------------
add_heading_1(doc, "4. MỤC 4.3: NĂM BIỂU ĐỒ THEN CHỐT (5 HEADLINE CHARTS) (~5-6 PHÚT)")
add_para(doc, "ĐÂY LÀ PHẦN TRỌNG TÂM ĂN ĐIỂM CAO NHẤT (Rubric 20%). Bạn cần đứng cạnh màn chiếu, dùng tay hoặc bút laser chỉ vào đúng vị trí của biểu đồ, đọc vanh vách các con số thực tế.")

# CHART 1
add_heading_2(doc, "CHART 1: PHÂN BỐ AQI THEO THÀNH PHỐ (HORIZONTAL BOXPLOT)")
add_para(doc, "Tiêu đề biểu đồ: Ahmedabad và các đô thị Bắc Ấn (Delhi, Gurugram, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor/Very Poor; chênh lệch gấp 5–13 lần so với Nam Ấn và Đông Bắc.")
add_stage_cue(doc, "Chỉ tay vào đỉnh biểu đồ nơi có thanh màu xanh dài của Ahmedabad, sau đó lia xuống nhóm Delhi, rồi lia xuống đáy biểu đồ nơi có Aizawl.")

speech_c1 = (
    "\"Bây giờ, em xin kính mời thầy cô và các bạn cùng nhìn vào Chart 1 — Biểu đồ hộp thể hiện phân bố AQI của 26 thành phố:\n\n"
    "Để mọi người dễ theo dõi, trục hoành là chỉ số AQI từ 0 đến 600, được nhóm em chia theo 6 dải màu cảnh báo chuẩn của Ấn Độ — "
    "từ Xanh lá (Good) đến Vàng (Moderate), Cam (Poor), Đỏ (Very Poor) và Tím sẫm (Severe). Hộp màu xanh thể hiện 50% số ngày điển hình (IQR), "
    "vạch thẳng đứng ở giữa là Trung vị (Median), hai râu kéo dài thể hiện phạm vi từ 5% đến 95% số ngày, và các dấu chấm là những ngày ngoại lai cực đoan.\n\n"
    "Nhìn vào biểu đồ này, điểm đập ngay vào mắt chúng ta là:\n"
    "- Ở ĐỈNH BIỂU ĐỒ: Thành phố Ahmedabad là 'quán quân ô nhiễm' tuyệt đối! Cả chiếc hộp IQR của Ahmedabad nằm trọn vẹn ở mức Poor đến Very Poor "
    "(từ 253 đến 484), với AQI trung vị lên tới 350.8, và có những chấm ngoại lai vọt lên kịch khung 600 ở mức Severe!\n"
    "- KẾ TIẾP LÀ DÀN ĐÔ THỊ ĐỒNG BẰNG SÔNG HẰNG PHÍA BẮC: Delhi đứng thứ hai với trung vị AQI là 236.9 (IQR từ 159 đến 328), "
    "Gurugram đứng thứ ba với 203.8, Lucknow đứng thứ tư với 191.6, và Patna với 167.8. Toàn bộ các đô thị này đều có chiếc hộp nằm sâu "
    "trong vùng cảnh báo nguy hiểm.\n"
    "- ĐỐI LẬP HOÀN TOÀN Ở ĐÁY BIỂU ĐỒ: Nhóm thành phố phía Nam và Đông Bắc như Aizawl có chiếc hộp bé tí nằm gọn lỏn trong vùng màu xanh an toàn, "
    "với AQI trung vị chỉ là 27.0, Shillong là 46.4, Thiruvananthapuram là 66.1. Hầu như quanh năm người dân ở đây không biết đến khái niệm ô nhiễm không khí!\n\n"
    "-> KẾT LUẬN CHART 1: Biểu đồ chứng minh ô nhiễm không khí tại Ấn Độ mang tính phân cực địa lý sâu sắc, chênh lệch giữa vùng trũng phía Bắc "
    "và vùng đồi núi/ven biển phía Nam lên tới 5 đến 13 lần!\""
)
add_callout(doc, speech_c1, title="LỜI THOẠI MẪU: CHART 1 (BOXPLOT AQI)", box_type="speech")

# CHART 2
add_heading_2(doc, "CHART 2: TỶ LỆ SỐ NGÀY THEO CẤP ĐỘ AQI (100% STACKED BAR CHART)")
add_para(doc, "Tiêu đề biểu đồ: Hơn 50%–87% số ngày tại Ahmedabad, Delhi, Gurugram ở mức kém (Poor) trở lên; trong khi Aizawl và Shillong có hơn 96%–100% ngày đạt chuẩn Good/Satisfactory.")
add_stage_cue(doc, "Chỉ vào thanh ngang trên cùng có dải màu đỏ/tím khổng lồ của Ahmedabad, sau đó chỉ xuống Delhi và các thành phố ở đáy.")

speech_c2 = (
    "\"Nếu Chart 1 cho chúng ta thấy con số trung vị, thì Chart 2 sẽ cho thấy gánh nặng sức khỏe tàn khốc mà người dân phải gánh chịu hàng ngày:\n\n"
    "Chart 2 là biểu đồ thanh xếp chồng 100%, mỗi thanh thể hiện tổng số ngày trong năm của từng thành phố, được sắp xếp từ trên xuống dưới "
    "theo tỷ lệ số ngày ô nhiễm độc hại (tức là tổng của 3 mức: Poor màu cam, Very Poor màu đỏ, và Severe màu tím sẫm).\n\n"
    "Hãy nhìn vào những con số giật mình trên biểu đồ:\n"
    "- Tại Ahmedabad: Có tới 87.1% số ngày trong năm rơi vào mức ô nhiễm đáng báo động! Trong đó mức nguy hại nhất là Severe chiếm tới 39.6%, "
    "Very Poor chiếm 25.6%. Số ngày người dân được hít thở không khí trong lành đạt chuẩn Good và Satisfactory chỉ vỏn vẹn đúng... 0.7%! "
    "Nghĩa là trong cả 365 ngày, họ chỉ có chưa đầy 3 ngày không khí sạch!\n"
    "- Tại thủ đô Delhi: Đứng thứ hai với 60.8% số ngày ở mức Poor trở lên (gồm 28.5% Poor, 23.9% Very Poor và 8.3% Severe). "
    "Tỷ lệ ngày đạt chuẩn an toàn của người dân Delhi chỉ có khiêm tốn 5.4%.\n"
    "- Tiếp theo là Gurugram với 51.1% ngày ô nhiễm, Lucknow 47.7%, Patna 43.6%.\n"
    "- Nhưng khi nhìn xuống đáy biểu đồ: Thành phố Aizawl đạt 100% ngày an toàn (Good chiếm 77.7%, Satisfactory 22.3%, hoàn toàn 0% ngày ô nhiễm). "
    "Coimbatore đạt 96.3% ngày an toàn, Shillong đạt 96.5%.\n\n"
    "-> KẾT LUẬN CHART 2: Đây là minh chứng đanh thép cho sự bất bình đẳng nghiêm trọng về phơi nhiễm y tế: Cùng sinh ra ở một đất nước, "
    "nhưng một đứa trẻ lớn lên ở Delhi hay Ahmedabad phải hít thở bụi độc trong suốt hơn 2/3 thời gian của năm, tạo nên gánh nặng khổng lồ "
    "cho hệ thống y tế công cộng!\""
)
add_callout(doc, speech_c2, title="LỜI THOẠI MẪU: CHART 2 (STACKED BAR)", box_type="speech")

# CHART 3
add_heading_2(doc, "CHART 3: QUY LUẬT MÙA VỤ BỤI MỊN PM2.5 (HEATMAP MONTH X CITY)")
add_para(doc, "Tiêu đề biểu đồ: Ô nhiễm PM2.5 mang tính mùa vụ cực đoan: bùng phát đỉnh điểm vào mùa đông (T11–T1) và chạm đáy vào mùa mưa (T7–T8) — Vượt xa quy chuẩn 24h quốc gia (60 µg/m³).")
add_stage_cue(doc, "Chỉ tay vào vệt màu đỏ rực ở góc bên phải (tháng 11-12) và góc bên trái (tháng 1) của Heatmap, rồi chỉ vào khoảng trắng/vàng nhạt ở giữa (tháng 7-8).")

speech_c3 = (
    "\"Kính thưa thầy cô, chuyển sang Chart 3, chúng ta sẽ bắt gặp một biểu đồ nhiệt (Heatmap) cực kỳ ấn tượng:\n\n"
    "Trục hoành là 12 tháng trong năm (từ Jan đến Dec), trục tung là các thành phố, và mỗi ô thể hiện nồng độ trung vị của bụi mịn PM2.5 (đơn vị µg/m³). "
    "Màu càng đỏ sẫm thì ô nhiễm càng nặng, màu vàng nhạt là an toàn.\n\n"
    "Chỉ cần nhìn lướt qua, mọi người sẽ thấy ngay một dải màu đỏ rực tạo thành hình chữ U bao trọn các tháng cuối năm và đầu năm:\n"
    "- Vệt đỏ bùng phát dữ dội từ tháng 10, đạt đỉnh điểm kinh hoàng vào THÁNG 11, THÁNG 12 VÀ THÁNG 1.\n"
    "- Hãy nhìn vào các con số kỷ lục trong từng ô: Tại Patna, tháng 12 nồng độ PM2.5 vọt lên tới 241.5 µg/m³! Tại Delhi, tháng 12 là 211.4 µg/m³ "
    "và tháng 11 là 204.6 µg/m³! Tại Lucknow là 194.0 µg/m³! Gurugram là 161.4 µg/m³!\n"
    "- Để mọi người dễ hình dung mức độ độc hại: Quy chuẩn quốc gia 24h của Ấn Độ là 60 µg/m³, còn ngưỡng an toàn của WHO chỉ là 15 µg/m³. "
    "Như vậy, vào mùa đông, người dân ở các đô thị này đang phải hít thở nồng độ bụi mịn vượt từ 3 đến 4 lần chuẩn quốc gia và gấp từ 13 đến 16 lần khuyến nghị của WHO!\n"
    "- Nhưng khi mùa mưa đến (tháng 7 và tháng 8): Toàn bộ ma trận nhiệt dịu hẳn xuống màu vàng nhạt và trắng. Delhi giảm từ 211 xuống chỉ còn 44.9 µg/m³! "
    "Patna giảm từ 241 xuống còn 40.1 µg/m³! Kolkata từ 120 xuống còn 23.0 µg/m³! Tức là nồng độ sụt giảm từ 5 đến 6 lần!\n\n"
    "-> KẾT LUẬN CHART 3: Ô nhiễm bụi mịn tại Ấn Độ không diễn ra đều đặn mà mang tính mùa vụ cực đoan. Mùa đông là giai đoạn báo động đỏ "
    "khi hiện tượng đốt rơm rạ sau thu hoạch kết hợp nghịch nhiệt khí quyển tạo nên những thảm họa sương mù quang hóa!\""
)
add_callout(doc, speech_c3, title="LỜI THOẠI MẪU: CHART 3 (HEATMAP PM2.5)", box_type="speech")

# CHART 4
add_heading_2(doc, "CHART 4: CHU KỲ BIẾN THIÊN 24 GIỜ (DUAL-PANEL DIURNAL CYCLE)")
add_para(doc, "Tiêu đề biểu đồ: Khí thải giao thông và nghịch nhiệt ban đêm tạo 2 đỉnh ô nhiễm sáng (8–10h) và đêm (20–23h); Ozone đạt đỉnh trưa chiều (13–15h) do phản ứng quang hóa.")
add_stage_cue(doc, "Chỉ sang Panel A (bên trái) chỉ 2 đỉnh của PM2.5, NO2, CO, rồi chỉ đường Ozone ngược pha; sau đó chỉ sang Panel B (bên phải) so sánh mùa đông và mùa mưa.")

speech_c4 = (
    "\"Tiếp theo là Chart 4 — một biểu đồ kép được nhóm em phân tích từ hơn 707 nghìn dòng dữ liệu giờ của bảng city_hour:\n\n"
    "Ở Panel A bên trái: Đây là chỉ số nồng độ đã được chuẩn hóa theo giờ của 4 chất đại diện (vạch đứt đoạn 1.0 chính là mức trung bình ngày).\n"
    "Hãy nhìn vào 3 chất phát thải sơ cấp là PM2.5 (đỏ), NO2 (đen) và CO (xám):\n"
    "- Cả 3 chất đều có mẫu hình HAI ĐỈNH NHỌN rất rõ rệt: Đỉnh sáng rơi vào khoảng 8h – 9h sáng (giờ cao điểm đi làm và đi học), "
    "và đỉnh đêm muộn rơi vào 20h – 22h đêm.\n"
    "- Đáng chú ý là đỉnh đêm muộn cao vượt trội so với đỉnh sáng: Nồng độ NO2 lúc 20h tối cao hơn mức trung bình ngày tới 41% (chỉ số 1.41); "
    "khí CO lúc 21h đêm cao hơn 69% (chỉ số 1.69); và PM2.5 lúc 22h-23h đêm cao hơn 20% (chỉ số 1.20).\n"
    "- Tại sao ban đêm không ai đi làm mà ô nhiễm lại cao nhất? Đó là vì chính quyền cho phép các đoàn xe tải hạng nặng chạy dầu diesel đi vào nội đô ban đêm, "
    "kết hợp với việc mặt đất nguội đi khiến tầng nghịch nhiệt hạ thấp, ép toàn bộ khói xe sát mặt đường!\n"
    "- ĐẶC BIỆT NHÌN VÀO ĐƯỜNG MÀU XANH DƯƠNG CỦA KHÍ OZONE (O3): Hoàn toàn ngược pha 180 độ! Ozone chạm đáy lúc 7h sáng (chỉ số 0.62), "
    "nhưng đến trưa chiều từ 13h đến 15h lại tăng dựng đứng đạt đỉnh cực đại gấp 1.61 lần trung bình ngày (cao hơn 61%)! "
    "Bởi vì Ozone tầng mặt đất là chất ô nhiễm thứ cấp, sinh ra từ phản ứng quang hóa khi có ánh nắng mặt trời chiếu gắt vào các oxit nitơ.\n\n"
    "Nhìn sang Panel B bên phải: Nhóm em tách riêng chu kỳ PM2.5 theo 4 mùa:\n"
    "- Mùa đông (đường màu xanh đậm) dao động với biên độ khổng lồ: Đêm lên tới 120.7 µg/m³ lúc 23h, sáng là 108.7 µg/m³, chiều hạ xuống 67.5 µg/m³.\n"
    "- Trong khi mùa mưa (đường màu xanh lá) nằm phẳng lì ở đáy, cả ngày đêm chỉ dao động nhẹ từ 32.9 đến 41.8 µg/m³, an toàn dưới chuẩn 60 µg/m³.\n\n"
    "-> LỜI KHUYÊN ĐẮT GIÁ: Người dân ở các đô thị miền Bắc không nên tập thể dục ngoài trời vào sáng sớm mùa đông (dễ hít trọn bụi độc) "
    "và cũng nên tránh ra đường vào đầu giờ chiều nắng gắt mùa hè (dễ hít phải khí Ozone kích ứng đường thở)!\""
)
add_callout(doc, speech_c4, title="LỜI THOẠI MẪU: CHART 4 (CHU KỲ 24H)", box_type="speech")

# CHART 5
add_heading_2(doc, "CHART 5: ĐÁNH GIÁ TÁC ĐỘNG ĐỢT PHONG TỎA COVID-19 (PAIRED BAR CHART)")
add_para(doc, "Tiêu đề biểu đồ: Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 35% và PM2.5 giảm 31% trên 19 thành phố; các đại đô thị ghi nhận mức giảm sâu nhất.")
add_stage_cue(doc, "Chỉ vào thanh ngang màu đen (NO2) và màu đỏ (PM2.5) của Ahmedabad, Kolkata, Delhi... rồi đặc biệt chỉ tay sang phía bên phải trục 0 nơi có Mumbai và Thiruvananthapuram.")

speech_c5 = (
    "\"Cuối cùng là Chart 5 — Một 'thí nghiệm tự nhiên' vô tiền khoáng hậu trong lịch sử môi trường:\n\n"
    "Vào mùa xuân năm 2020, Ấn Độ áp dụng lệnh phong tỏa toàn quốc nghiêm ngặt nhất thế giới để chống dịch COVID-19. "
    "Nhóm em đã đối chiếu nồng độ trung bình trong giai đoạn phong tỏa (25/3 đến 31/5/2020) so với đúng cùng kỳ năm 2019 "
    "trên 19 thành phố có trạm đo liên tục ở cả hai năm:\n\n"
    "Những con số biết nói trên biểu đồ:\n"
    "- Tính bình quân trên cả 19 thành phố (hai đường kẻ nét đứt): Khí NO2 sụt giảm trung bình 35.4% và bụi mịn PM2.5 giảm 30.7%.\n"
    "- TẠI SAO NO2 LẠI GIẢM SÂU HƠN PM2.5? Vì NO2 chủ yếu sinh ra từ động cơ xe cộ. Khi toàn bộ ô tô, xe máy bị cấm lưu thông, "
    "nồng độ NO2 lập tức rơi tự do! Trong khi PM2.5 giảm chậm hơn vì các nhà máy nhiệt điện than và bếp đun sinh hoạt ở nông thôn vẫn hoạt động.\n"
    "- Hãy nhìn vào các thành phố có mức giảm kỷ lục: Tại Ahmedabad, NO2 giảm tới 66.5% và PM2.5 giảm 59.1%! Tại Kolkata, NO2 giảm 59.4% và PM2.5 giảm 40.0%! "
    "Tại Lucknow, NO2 giảm 53.9%! Tại thủ đô Delhi, NO2 giảm 46.5% và PM2.5 giảm 37.0%!\n\n"
    "- VÀ ĐÂY LÀ ĐIỂM THỂ HIỆN TINH THẦN KHOA HỌC DỮ LIỆU CỦA NHÓM EM — NHÌN VÀO CÁC NGOẠI LỆ Ở BÊN PHẢI TRỤC 0:\n"
    "+ Tại Mumbai: Mặc dù NO2 giảm 38.2%, nhưng PM2.5 lại tăng 30.7%! Nhóm em đã tìm hiểu và nhận thấy trong giai đoạn này, "
    "các hoạt động công nghiệp cảng biển ngoại vi và điều kiện vi khí hậu ven biển khô hạn đã khiến bụi nền không thể phân tán.\n"
    "+ Tại Thiruvananthapuram: Cột NO2 vọt sang phải tới 93.3%. Lý do kỹ thuật là vì trong năm 2019 trạm ở đây đo rất ít ngày, "
    "sang 2020 số ngày đo đầy đủ hơn và có nguồn phát thải cục bộ gần vị trí đặt trạm quan trắc.\n\n"
    "-> KẾT LUẬN CHART 5: Đợt phong tỏa chứng minh rằng: Nếu chúng ta có chính sách quyết liệt hạn chế phát thải từ phương tiện giao thông "
    "và chuyển đổi sang xe điện, bầu trời hoàn toàn có thể xanh trở lại trong một thời gian rất ngắn!\""
)
add_callout(doc, speech_c5, title="LỜI THOẠI MẪU: CHART 5 (LOCKDOWN COVID-19)", box_type="speech")

# ----------------- SECTION 5: 4.4 TỔNG KẾT & PHÁT HIỆN -----------------
add_heading_1(doc, "5. MỤC 4.4: ĐÚC KẾT 5 PHÁT HIỆN THEN CHỐT & KHUYẾN NGHỊ CHÍNH SÁCH (~1.5 PHÚT)")
add_para(doc, "Mục tiêu: Đúc kết lại thành 5 thông điệp đắt giá gắn liền với thực tiễn xã hội, chuẩn bị chuyển giao sang phần mô hình Machine Learning.")
add_stage_cue(doc, "Chiếu slide bảng tổng kết 5 phát hiện then chốt.")

speech_44 = (
    "\"Để tóm gọn lại toàn bộ Phần 4, nhóm em xin đúc kết lại 5 thông điệp then chốt và các khuyến nghị thực tiễn:\n\n"
    "1. Tâm điểm ô nhiễm nằm ở đồng bằng sông Hằng và Tây Ấn (Ahmedabad trung vị 350.8, Delhi 236.9, Gurugram, Lucknow, Patna) với chỉ số AQI cao gấp 5-13 lần Nam Ấn. "
    "Khuyến nghị: Không thể quản lý theo ranh giới hành chính của từng thành phố riêng lẻ, mà phải quản lý chất lượng không khí theo "
    "toàn bộ lưu vực khí quyển (Airshed Management) có sự phối hợp liên bang!\n\n"
    "2. Bất bình đẳng phơi nhiễm y tế: Người dân Ahmedabad chịu tới 87.1% ngày ô nhiễm (trong đó 39.6% là Severe, chỉ 0.7% ngày an toàn), Delhi chịu hơn 60.8% ngày Poor trở lên, trong khi Aizawl đạt 100% an toàn. "
    "Khuyến nghị: Ưu tiên ngân sách y tế dự phòng, phát khẩu trang N95 và lắp đặt hệ thống lọc khí tại các trường học, bệnh viện miền Bắc.\n\n"
    "3. Tính mùa vụ cực đoan: Mùa đông nồng độ bụi PM2.5 bùng phát (Patna 241.5 µg/m³, Delhi 211.4 µg/m³), tăng gấp 5-6 lần mùa mưa do nghịch nhiệt 'nắp nồi' tầng biên. "
    "Khuyến nghị: Kế hoạch hành động khẩn cấp (như hạn chế xe cơ giới, cấm đốt rơm rạ) phải được kích hoạt sớm ngay từ tháng 10 hàng năm, "
    "chứ không nên đợi đến khi trời mù mịt vào tháng 12 mới ứng phó.\n\n"
    "4. Quy luật phát thải 2 đỉnh giao thông sáng/đêm và đỉnh Ozone buổi trưa: Đỉnh đêm (20h-22h) cao hơn đỉnh sáng (NO2 cao hơn 41%, CO cao hơn 69%) do xe tải nặng vào nội đô; còn Ozone đạt đỉnh lúc 14h-15h chiều (+61%) do quang hóa. "
    "Khuyến nghị: Cấm xe tải nặng vào nội đô ban đêm, và khuyến cáo người dân tránh tập thể dục sáng sớm mùa đông hoặc ra đường lúc trưa nắng gắt.\n\n"
    "5. Bằng chứng từ COVID-19: Khi đóng băng hoạt động kinh tế, NO2 giảm trung bình 35.4% và PM2.5 giảm 30.7% (Ahmedabad giảm tới 66.5% NO2 và 59.1% PM2.5). Ngoại lệ tại Mumbai (+30.7% PM2.5) phản ánh tính chất cảng biển và thời tiết ven biển. "
    "Khuyến nghị: Minh chứng không khí hoàn toàn có thể cải thiện nhanh chóng nếu quyết liệt điện hóa xe buýt công cộng, mở rộng Metro và nâng chuẩn khí thải.\n\n"
    "Đặc biệt, phân tích nhóm còn chỉ ra: Hiệu ứng cuối tuần hầu như vắng bóng (PM2.5 chỉ giảm 0.58%), chứng minh ô nhiễm bị chi phối bởi phát thải nền 24/7 (nhiệt điện than, đun nấu sinh khối) và thời gian bụi lơ lửng 5-7 ngày!\""
)
add_callout(doc, speech_44, title="LỜI THOẠI MẪU: ĐÚC KẾT & KHUYẾN NGHỊ", box_type="speech")

# ----------------- SECTION 6: KẾT THÚC & Q&A -----------------
add_heading_1(doc, "6. GIỚI HẠN DỮ LIỆU & LỜI KẾT (~0.5 PHÚT)")
add_stage_cue(doc, "Nói với thái độ khiêm tốn, cầu thị và chuyên nghiệp.")

speech_end = (
    "\"Kính thưa thầy cô, trước khi kết thúc phần 4, nhóm em cũng xin thẳng thắn nhìn nhận 3 giới hạn của bộ dữ liệu này:\n"
    "- Thứ nhất (Độ phủ): Dữ liệu tập trung ở 26 thành phố lớn, chưa bao phủ hết các vùng nông thôn và đô thị vệ tinh.\n"
    "- Thứ hai (Khí tượng): Dữ liệu chưa có các thông số vi khí hậu quan trọng như nhiệt độ, độ ẩm, tốc độ gió và chiều cao tầng nghịch nhiệt.\n"
    "- Thứ ba (Thời gian): Dữ liệu năm 2020 chỉ ghi nhận đến tháng 7/2020, cần tránh ngộ nhận rằng không khí đã được cải thiện bền vững.\n"
    "Chính vì vậy, sang Phần 5 tiếp theo, nhóm em sẽ tận dụng các phát hiện từ EDA này để kiến trúc các đặc trưng trễ (Lag features 1h, 24h, 7 ngày), "
    "đặc trưng chu kỳ thời gian (Cyclical encoding sin/cos cho giờ và tháng) và xây dựng các mô hình học máy (Machine Learning) "
    "nhằm dự báo chính xác chỉ số AQI và nồng độ bụi mịn một cách thông minh nhất.\n\n"
    "Em xin chân thành cảm ơn thầy cô và các bạn đã chú ý lắng nghe bài trình bày của nhóm em. "
    "Bây giờ, nhóm em rất mong nhận được những câu hỏi và góp ý quý báu từ thầy cô ạ!\""
)
add_callout(doc, speech_end, title="LỜI THOẠI MẪU: KẾT THÚC BÀI THUYẾT TRÌNH", box_type="speech")

# ----------------- SECTION 7: BỘ HỎI ĐÁP PHẢN BIỆN (FAQ) -----------------
add_heading_1(doc, "7. BỘ CÂU HỎI PHẢN BIỆN THƯỜNG GẶP CỦA GIẢNG VIÊN (FAQ)")
add_para(doc, "Khi bạn thuyết trình xong, các thầy cô dạy Data Science thường sẽ hỏi xoáy vào bản chất thống kê. Dưới đây là 5 câu hỏi kinh điển và câu trả lời 'chuẩn bài' nhất:")

faq_list = [
    (
        "Câu hỏi 1: 'Tại sao nhóm lại kiên quyết dùng Median (Trung vị) và IQR thay vì Mean (Trung bình) và Độ lệch chuẩn (Std)?'",
        "Trả lời ngắn gọn & chuẩn xác:\n"
        "\"Dạ thưa thầy/cô, trong Slide 16 của môn học về họ số đo Shape, chúng em đã kiểm tra và thấy dữ liệu chất lượng không khí bị lệch phải rất mạnh "
        "(Skewness của AQI là 2.81, CO lên tới 7.53) và có đuôi rất dày (Kurtosis rất cao). "
        "Trong thống kê, số Trung bình (Mean) rất nhạy cảm và dễ bị bóp méo bởi các giá trị ngoại lai cực đoan trong các ngày sương mù mùa đông. "
        "Do đó, Median và IQR là các thước đo phi tham số có tính kháng nhiễu (robust statistics), phản ánh đúng nhất mức độ ô nhiễm thông thường mà đại đa số người dân phải trải qua hàng ngày ạ!\""
    ),
    (
        "Câu hỏi 2: 'Tại sao trên Chart 1, thành phố Ahmedabad lại có AQI cao vượt trội hơn cả thủ đô Delhi?'",
        "Trả lời:\n"
        "\"Dạ thưa thầy/cô, Ahmedabad là một trung tâm công nghiệp nặng, dệt may và hóa chất cực kỳ sầm uất tại bang Gujarat. "
        "Trạm quan trắc tại Ahmedabad đặt gần các khu vực tập trung sản xuất công nghiệp và các nút giao vận tải lớn. "
        "Hơn nữa, khí hậu của Ahmedabad là bán khô hạn, lượng mưa hàng năm rất thấp nên bụi lơ lửng trong không khí hầu như không được rửa trôi, "
        "dẫn đến chỉ số AQI trung vị lên tới 350.8, cao nhất cả nước trong tập dữ liệu này ạ.\""
    ),
    (
        "Câu hỏi 3: 'Tại sao cuối tuần lượng xe đi lại ít hơn mà nồng độ bụi và AQI lại không giảm?'",
        "Trả lời:\n"
        "\"Dạ thưa thầy/cô, điều này thể hiện bản chất đa nguồn của ô nhiễm không khí tại Ấn Độ. Xe cá nhân chỉ chiếm một phần phát thải. "
        "Các nguồn phát thải khổng lồ khác như các nhà máy nhiệt điện than, đốt rác nông nghiệp, đun nấu sinh khối bằng củi than của hàng triệu hộ gia đình "
        "và các đoàn xe tải liên tỉnh vẫn chạy đều đặn 7 ngày trong tuần. "
        "Thêm vào đó, bụi PM2.5 có kích thước vi mô siêu nhẹ, thời gian lưu trong khí quyển kéo dài từ 5 đến 7 ngày, nên 2 ngày nghỉ cuối tuần "
        "là quá ngắn để tạo ra sự khác biệt đo lường được ạ.\""
    ),
    (
        "Câu hỏi 4: 'Tại sao trên Chart 5 về Lockdown, nồng độ PM2.5 ở Mumbai và NO2 ở Thiruvananthapuram lại tăng thay vì giảm?'",
        "Trả lời (Ăn điểm tuyệt đối vì đã chuẩn bị kỹ ngoại lệ):\n"
        "\"Dạ thưa thầy/cô, đây chính là chi tiết nhóm em rất tâm đắc khi quan sát biểu đồ:\n"
        "- Ở Mumbai, mặc dù giao thông nội đô dừng hẳn làm NO2 giảm 38.2%, nhưng PM2.5 lại tăng 30.7%. Nhóm em tìm hiểu thì thấy tháng 4-5/2020, "
        "Mumbai chịu ảnh hưởng của các đợt gió khô mang bụi từ sa mạc Thar thổi qua, kết hợp với các cảng biển và cơ sở công nghiệp thiết yếu vẫn hoạt động.\n"
        "- Ở Thiruvananthapuram, cột NO2 tăng 93.3% là do yếu tố dữ liệu: năm 2019 trạm này đo gián đoạn rất ít ngày nền thấp, sang 2020 số ngày đo đầy đủ hơn "
        "và trạm đặt gần các trục đường vận chuyển hàng hóa thiết yếu trong dịch. "
        "Việc nhìn thẳng vào các ngoại lệ này giúp nhóm em hiểu rằng không thể áp đặt một kết luận duy ý chí cho mọi địa phương ạ.\""
    ),
    (
        "Câu hỏi 5: 'Tại sao khí Ozone (O3) lại đạt đỉnh vào đầu giờ chiều (13h-15h) trong khi các chất khác lại chạm đáy?'",
        "Trả lời:\n"
        "\"Dạ thưa thầy/cô, các chất như PM2.5, NO2, CO là chất ô nhiễm sơ cấp (primary pollutants), phát thải trực tiếp từ ống xả xe và hoạt động sinh hoạt. "
        "Vào đầu giờ chiều, nhiệt độ mặt đất cao làm đối lưu xáo trộn không khí mạnh, thổi bốc bụi lên cao nên nồng độ sát đất chạm đáy.\n"
        "Ngược lại, Ozone tầng mặt đất là chất ô nhiễm thứ cấp (secondary pollutant). Khí Ozone không phát ra trực tiếp từ ống xả, "
        "mà được sinh ra do phản ứng quang hóa giữa oxit nitơ (NOx) và các hợp chất hữu cơ dễ bay hơi (VOCs) dưới tác động của bức xạ cực tím từ ánh nắng mặt trời. "
        "Khung giờ 13h - 15h là lúc ánh nắng mặt trời gay gắt nhất trong ngày, thúc đẩy phản ứng quang hóa đạt tốc độ cực đại, khiến Ozone tăng vọt lên đỉnh ạ!\""
    )
]

for q_title, q_ans in faq_list:
    add_callout(doc, q_ans, title=q_title, box_type="qa")

# ----------------- SECTION 8: BẢNG TRA CỨU SỐ LIỆU ĐỐI CHIẾU -----------------
add_heading_1(doc, "8. BẢNG TRA CỨU SỐ LIỆU NHANH ĐỂ KHÔNG BAO GIỜ BỊ QUÊN KHI THUYẾT TRÌNH")
add_para(doc, "Bảng tóm tắt các con số chuẩn xác nhất của từng biểu đồ, bạn có thể in ra một tờ giấy cầm tay khi lên thuyết trình:")

table_data = [
    ["Hạng mục / Biểu đồ", "Con số then chốt cần nhớ", "Thông điệp chính"],
    ["4.1 Bốn họ số đo", "PM2.5 median: 48.4 µg/m³ | AQI median: 115.3 | Mean: 161.9 | CO CV: 253%", "Dữ liệu lệch phải mạnh -> Phải dùng Median & IQR"],
    ["Chart 1 (Boxplot)", "Top 1: Ahmedabad (Median 350.8, IQR 253-484)\nDelhi (236.9) | Đáy: Aizawl (27.0)", "Phân cực Bắc - Nam, chênh lệch giữa đỉnh và đáy gấp 13 lần"],
    ["Chart 2 (Stacked Bar)", "Ahmedabad: 87.1% Poor+ (39.6% Severe)\nDelhi: 60.8% Poor+ (Good/Sat chỉ 5.4%)\nAizawl: 100% an toàn", "Bất bình đẳng phơi nhiễm y tế tàn khốc giữa các đô thị"],
    ["Chart 3 (Heatmap)", "Tháng 11-1: Patna (241.5), Delhi (211.4), Lucknow (194.0)\nTháng 7-8: Giảm còn 23 - 45 µg/m³", "Mùa đông vượt chuẩn Ấn Độ 3-4 lần, gấp 13-16 lần WHO. Mùa mưa giảm 5-6 lần"],
    ["Chart 4 (Diurnal 24h)", "PM2.5/NO2/CO: 2 đỉnh sáng 8-9h & đêm 20-22h\nOzone ngược pha: đỉnh 14-15h chiều (+61%)\nMùa đông đêm: 120.7 µg/m³ | Mưa: 33-42 µg/m³", "Nghịch nhiệt & xe tải ban đêm ép khói độc; Ozone quang hóa trưa nắng"],
    ["Chart 5 (Lockdown)", "Trung bình 19 thành phố: NO2 giảm 35.4%, PM2.5 giảm 30.7%\nAhmedabad: NO2 -66.5%, PM2.5 -59.1%\nNgoại lệ: Mumbai PM2.5 +30.7%", "NO2 giảm mạnh hơn do xe ngừng chạy; chứng minh chính sách giao thông xanh là khả thi"]
]

tbl = doc.add_table(rows=len(table_data), cols=3)
tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl.autofit = False

col_widths = [Inches(1.8), Inches(2.7), Inches(2.2)]
for r_idx, row in enumerate(tbl.rows):
    for c_idx, cell in enumerate(row.cells):
        cell.width = col_widths[c_idx]
        set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(table_data[r_idx][c_idx])
        r.font.name = 'Calibri'
        
        if r_idx == 0:
            set_cell_background(cell, "1B365D")
            r.bold = True
            r.font.size = Pt(10)
            r.font.color.rgb = RGBColor(255, 255, 255)
        else:
            if r_idx % 2 == 1:
                set_cell_background(cell, "F9FBFD")
            else:
                set_cell_background(cell, "FFFFFF")
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_DARK
            if c_idx == 0:
                r.bold = True

output_path = Path('reports/Kich_ban_thuyet_trinh_Phan_4_EDA.docx')
doc.save(output_path)
print(f"Successfully created: {output_path}")

# Copy to workspace root for easy access
root_path = Path('Kich_ban_thuyet_trinh_Phan_4_EDA.docx')
shutil.copyfile(output_path, root_path)
print(f"Copied to workspace root: {root_path}")
