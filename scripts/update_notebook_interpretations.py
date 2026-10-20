import json

def update_notebook(nb_path):
    print(f"Updating {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for i, c in enumerate(nb['cells']):
        if c.get('cell_type') != 'markdown':
            continue
        text = ''.join(c.get('source', []))

        # Cell 12: Nhóm Thành phố
        if '**Nhận xét phân tích nhóm Thành phố:**' in text:
            new_text = (
                "**Nhận xét phân tích nhóm Thành phố:**\n"
                "- **Ahmedabad và các đô thị đồng bằng sông Hằng là tâm điểm ô nhiễm:** "
                "Thành phố công nghiệp phía Tây **Ahmedabad** đứng đầu bảng với mức độ ô nhiễm kỷ lục (AQI trung bình 398.8, AQI trung vị 350.8, 87.1% ngày ở mức Poor trở lên). "
                "Kế tiếp là các đại đô thị đồng bằng sông Hằng phía Bắc gồm **Delhi (AQI trung vị 236.9, 60.8% ngày Poor trở lên)**, **Gurugram (203.8, 51.1% ngày Poor+)**, "
                "**Lucknow (191.6, 47.7% ngày Poor+)** và **Patna (167.8, 43.6% ngày Poor+)**.\n"
                "- **Khu vực không khí trong lành:** Các thành phố ven biển Nam Ấn và vùng núi Đông Bắc như "
                "**Aizawl (AQI trung vị 27.0)**, **Shillong (46.4)**, **Thiruvananthapuram (66.1)**, **Coimbatore (73.5)** và **Amaravati (74.7)** "
                "có tỷ lệ ngày đạt chuẩn Good/Satisfactory vượt trên 86%–100%, hầu như không xuất hiện ngày ô nhiễm mức Poor.\n"
                "- **Sự khác biệt giữa các siêu đô thị:** Dù có mật độ dân số và xe cộ khổng lồ, Mumbai (AQI trung vị 90.4) và Chennai (97.2) "
                "có chỉ số AQI thấp hơn Delhi tới **hơn 2.4 đến 2.6 lần** nhờ vị trí địa lý ven biển có gió biển thổi liên tục giúp khuếch tán chất ô nhiễm."
            )
            c['source'] = [new_text]

        # Cell 18: Nhóm Mùa vụ
        elif '**Nhận xét phân tích nhóm Mùa vụ:**' in text:
            new_text = (
                "**Nhận xét phân tích nhóm Mùa vụ:**\n"
                "- **Mùa đông (Tháng 12 – Tháng 2) là thời kỳ đen tối nhất:** "
                "AQI trung vị toàn quốc lên tới **172.8** (trung bình là **220.8**), PM2.5 trung vị **74.0 µg/m³**, và **42.4% số ngày rơi vào mức Poor trở lên**.\n"
                "- **Mùa mưa gió mùa (Tháng 6 – Tháng 9) là thời điểm trong lành nhất:** "
                "AQI trung vị giảm sâu xuống **90.4**, PM2.5 trung vị chỉ còn **33.1 µg/m³**, và tỷ lệ ngày Poor giảm chỉ còn **9.0%** nhờ nước mưa rửa trôi hạt bụi (*wet scavenging*).\n"
                "- **Hệ số Mùa Đông / Mùa Mưa:** Mức chênh lệch lớn nhất cả nước không phải là Delhi mà thuộc về **Guwahati (gấp 6.17 lần - từ 46.3 mùa mưa lên 285.4 mùa đông)**, "
                "tiếp theo là **Kolkata (gấp 4.34 lần)**, **Patna (gấp 3.77 lần)**, **Lucknow (gấp 3.28 lần)**, và **Delhi (gấp 2.37 lần)**.\n"
                "- **Cơ chế khí quyển:** Vào mùa đông, thời tiết lạnh kèm gió yếu gây ra hiện tượng **nghịch nhiệt tầng biên (*boundary layer inversion*)**, "
                "tạo thành một chiếc 'nắp nồi' nhiệt nhốt chặt toàn bộ khí thải giao thông và khói đốt rơm rạ sát mặt đất."
            )
            c['source'] = [new_text]

        # Cell 31: Diễn giải Chart 1
        elif '**Diễn giải Chart 1:**' in text:
            new_text = (
                "**Diễn giải Chart 1:**\n"
                "- **Ahmedabad ở đỉnh bảng ô nhiễm:** Hộp tứ phân vị (IQR từ 25% đến 75%) của Ahmedabad nằm trọn vẹn từ 253.5 đến 483.7 với AQI trung vị lên tới **350.8** (mức Very Poor), "
                "và xuất hiện nhiều điểm ngoại lai chạm ngưỡng kịch khung 600 (Severe).\n"
                "- **Nhóm đồng bằng sông Hằng Bắc Ấn ô nhiễm nghiêm trọng:** Delhi (AQI trung vị **236.9**, IQR 159.0–328.1), Gurugram (**203.8**), Lucknow (**191.6**) và Patna (**167.8**) "
                "đều có hộp IQR nằm sâu trong vùng Poor và Very Poor.\n"
                "- **Phân cực địa lý sâu sắc so với miền Nam và Đông Bắc:** Các thành phố ở đáy biểu đồ như Aizawl (AQI trung vị **27.0**), Shillong (**46.4**), Thiruvananthapuram (**66.1**) "
                "và Coimbatore (**73.5**) có hộp IQR nằm gọn trong vùng an toàn Good và Satisfactory. Khoảng cách chênh lệch giữa đỉnh và đáy lên tới **13 lần**."
            )
            c['source'] = [new_text]

        # Cell 34: Diễn giải Chart 2
        elif '**Diễn giải Chart 2:**' in text:
            new_text = (
                "**Diễn giải Chart 2:**\n"
                "- **Gánh nặng ô nhiễm cực đoan tại Ahmedabad và Delhi:**\n"
                "  + Tại Ahmedabad, có tới **87.1% số ngày trong năm** rơi vào mức ô nhiễm đáng báo động (trong đó Severe chiếm **39.6%**, Very Poor chiếm **25.6%**, Poor chiếm **21.9%**); "
                "số ngày người dân được hít thở không khí an toàn (Good/Satisfactory) chỉ vỏn vẹn **0.7%** (chưa đầy 3 ngày trong cả năm!).\n"
                "  + Tại Delhi, có tới **60.8% số ngày** ở mức Poor trở lên (Poor 28.5%, Very Poor 23.9%, Severe 8.3%), trong khi tỷ lệ ngày đạt chuẩn an toàn chỉ vỏn vẹn **5.4%**.\n"
                "  + Các đô thị lân cận cũng chịu chung số phận: Gurugram có **51.1% ngày Poor+**, Lucknow **47.7%**, Patna **43.6%**.\n"
                "- **Đối lập tuyệt đối ở nhóm sạch:** Aizawl đạt **100% số ngày an toàn** (Good chiếm 77.7%, Satisfactory 22.3%, hoàn toàn không có ngày nào vượt quá Satisfactory). "
                "Coimbatore đạt **96.3% ngày an toàn**, Shillong đạt **96.5%**.\n"
                "- **Ý nghĩa y tế:** Bằng chứng cho thấy sự bất bình đẳng phơi nhiễm y tế tàn khốc — người dân tại Bắc Ấn và Ahmedabad phải hít thở không khí độc hại suốt hơn 2/3 thời gian của năm."
            )
            c['source'] = [new_text]

        # Cell 37: Diễn giải Chart 3
        elif '**Diễn giải Chart 3:**' in text:
            new_text = (
                "**Diễn giải Chart 3:**\n"
                "- **Hình thái chữ U đỏ rực mùa đông:** Nồng độ PM2.5 theo tháng bộc lộ hình chữ U rõ rệt: tăng vọt từ tháng 10, đạt đỉnh cực đại vào **tháng 11, tháng 12 và tháng 1**, "
                "sau đó giảm sâu vào mùa mưa **tháng 7, tháng 8 và tháng 9**.\n"
                "- **Các kỷ lục nồng độ mùa đông:** Patna ghi nhận đỉnh điểm vào tháng 12 lên tới **241.5 µg/m³** (tháng 11 là 206.9 µg/m³); Delhi tháng 12 là **211.4 µg/m³** (tháng 11 là 204.6 µg/m³); "
                "Lucknow tháng 11 là **195.7 µg/m³** và tháng 12 là **194.0 µg/m³**; Gurugram tháng 12 là **161.4 µg/m³**.\n"
                "- **Đối chiếu quy chuẩn:** Mức nồng độ này vượt từ **3 đến 4 lần quy chuẩn quốc gia 24h của Ấn Độ (60 µg/m³)** và gấp từ **13 đến 16 lần khuyến nghị của WHO (15 µg/m³)**.\n"
                "- **Mùa mưa giải cứu không khí:** Vào tháng 7 và 8, nồng độ PM2.5 tại Delhi giảm xuống **44.9–49.6 µg/m³**, Patna còn **40.1–42.0 µg/m³**, Lucknow còn **35.7–36.1 µg/m³**, "
                "Kolkata giảm xuống **23.0 µg/m³** — mức chênh lệch giữa mùa đông và mùa mưa lên tới **5 đến 6 lần**."
            )
            c['source'] = [new_text]

        # Cell 40: Diễn giải Chart 4
        elif '**Diễn giải Chart 4:**' in text:
            new_text = (
                "**Diễn giải Chart 4:**\n"
                "- **Panel A (Mẫu hình theo giờ chuẩn hóa):**\n"
                "  + Các chất phát thải sơ cấp (PM2.5, NO2, CO) có 2 đỉnh nhọn rõ rệt: Đỉnh sáng lúc **8h–9h** (giờ cao điểm giao thông) và đỉnh đêm muộn lúc **20h–22h**.\n"
                "  + Đỉnh đêm muộn cao vượt trội do xe tải nặng vào nội đô kết hợp lớp nghịch nhiệt ban đêm ép bụi xuống mặt đất: "
                "NO2 lúc 20h tối cao hơn trung bình ngày tới **41%** (chỉ số 1.41); CO lúc 21h đêm cao hơn **69%** (chỉ số 1.69); PM2.5 lúc 22h–23h cao hơn **20%** (chỉ số 1.20).\n"
                "  + Đáy nồng độ của bụi rơi vào **15h–17h** chiều khi đối lưu bốc cao khuếch tán chất ô nhiễm.\n"
                "  + **Ozone (O3) hoàn toàn ngược pha:** Chạm đáy lúc 7h sáng (0.62) và tăng vọt đạt đỉnh vào **14h–15h chiều (1.61, cao hơn trung bình ngày 61%)** do phản ứng quang hóa khi có ánh nắng mặt trời gay gắt.\n"
                "- **Panel B (Khác biệt mùa vụ):** Mẫu hình chu kỳ tồn tại ở cả 4 mùa, nhưng biên độ mùa đông vượt trội hoàn toàn: "
                "PM2.5 đêm mùa đông lên tới **120.7 µg/m³ (lúc 23h)** và sáng là 108.7 µg/m³; trong khi mùa mưa đường biểu đồ nằm bẹp ở đáy, cả ngày đêm chỉ dao động nhẹ từ **32.9 đến 41.8 µg/m³**, luôn an toàn dưới quy chuẩn 60 µg/m³."
            )
            c['source'] = [new_text]

        # Cell 43: Diễn giải Chart 5
        elif '**Diễn giải Chart 5:**' in text:
            new_text = (
                "**Diễn giải Chart 5:**\n"
                "- **Tổng thể trên 19 thành phố đối chiếu:** Giai đoạn phong tỏa toàn quốc nghiêm ngặt làm **NO2 giảm trung bình 35.4% và PM2.5 giảm 30.7%** so với cùng kỳ 2019.\n"
                "- **NO2 sụt giảm sâu hơn PM2.5:** NO2 gắn liền với khí thải phương tiện giao thông nên khi lệnh cấm di chuyển có hiệu lực, nồng độ NO2 sụt giảm tức thì 50%–66% tại các thành phố lớn "
                "(Ahmedabad giảm **-66.5%**, Kolkata **-59.4%**, Amaravati **-55.8%**, Lucknow **-53.9%**, Jaipur **-51.4%**, Delhi **-46.5%**, Chennai **-45.1%**). "
                "PM2.5 giảm chậm hơn do vẫn còn nguồn phát thải nền từ các nhà máy điện than và nấu nướng sinh hoạt.\n"
                "- **Nhận diện chính xác các ngoại lệ bên phải trục 0:**\n"
                "  + Tại **Mumbai**, NO2 giảm -38.2% nhưng PM2.5 lại tăng **+30.7%** do các hoạt động công nghiệp cảng biển duy trì và điều kiện thời tiết khô hạn ven biển trong tháng 4-5/2020.\n"
                "  + Tại **Thiruvananthapuram**, cột NO2 tăng **+93.3%** do năm 2019 trạm đo gián đoạn ít ngày, sang 2020 đo đầy đủ hơn kết hợp nguồn phát thải cục bộ gần vị trí đặt trạm."
            )
            c['source'] = [new_text]

        # Cell 44: Bảng tổng kết 5 phát hiện then chốt
        elif 'Bảng tổng hợp **5 phát hiện then chốt gắn liền với 5 biểu đồ**' in text:
            new_text = (
                "## 4.4. Tổng kết & Phát hiện then chốt (*Key Findings tied directly to Headline Charts*)\n\n"
                "Bảng tổng hợp **5 phát hiện then chốt gắn liền với 5 biểu đồ**, phục vụ trực tiếp cho **Mục 5 (Key Findings)** và **Mục 6 (Limitations)** trong Slide báo cáo:\n\n"
                "| # | Phát hiện then chốt (*Key Finding*) | Biểu đồ minh chứng | Ý nghĩa thực tiễn & Khuyến nghị chính sách |\n"
                "|---|-------------------------------------|-------------------|---------------------------------------------|\n"
                "| **1** | **Ahmedabad và Bắc Ấn là tâm điểm ô nhiễm:** Ahmedabad dẫn đầu cả nước (AQI trung vị 350.8), tiếp theo là các đô thị đồng bằng sông Hằng (Delhi 236.9, Gurugram 203.8, Lucknow 191.6, Patna 167.8), cao gấp **5–13 lần** các đô thị ven biển Nam Ấn và đồi núi Đông Bắc. | **Chart 1** | Cần chính sách kiểm soát chất lượng không khí theo lưu vực khí quyển (*Airshed Management*), phối hợp liên vùng thay vì quản lý đơn lẻ theo ranh giới hành chính từng thành phố. |\n"
                "| **2** | **Bất bình đẳng về phơi nhiễm y tế:** Người dân tại Ahmedabad và Delhi phải chịu từ **61% đến 87% số ngày trong năm** với không khí ở mức Poor trở lên (trong đó Ahmedabad có 39.6% ngày Severe); ngược lại Aizawl có **100% ngày đạt chuẩn an toàn** (Good/Satisfactory). | **Chart 2** | Ưu tiên trang bị hệ thống lọc không khí y tế dự phòng và cảnh báo nguy cơ hô hấp cho người già và trẻ nhỏ tại các đô thị miền Bắc và Ahmedabad. |\n"
                "| **3** | **Tính mùa vụ cực đoan:** Ô nhiễm PM2.5 bùng phát đỉnh điểm vào mùa đông (T11–T1) với nồng độ tại Patna, Delhi, Lucknow đạt 194–241 µg/m³ (gấp **3–4 lần quy chuẩn quốc gia**, gấp **13–16 lần WHO**), và chạm đáy vào mùa mưa (T7–T8). | **Chart 3** | Hiện tượng nghịch nhiệt mùa đông khuếch đại nồng độ phát thải. Các biện pháp khẩn cấp (hạn chế phương tiện, dừng thi công, kiểm soát đốt rơm rạ) phải được kích hoạt sớm từ tháng 10 hàng năm. |\n"
                "| **4** | **Quy luật phát thải 2 đỉnh giao thông & pha quang hóa Ozone:** PM2.5, NO2, CO đạt 2 đỉnh nhọn vào sáng sớm (8–9h) và đêm muộn (20–22h, NO2 cao hơn 41%, CO cao hơn 69%); Ozone đạt đỉnh vào đầu giờ chiều (14–15h, cao hơn 61%). | **Chart 4** | Khuyến cáo người dân tránh tập thể dục ngoài trời vào sáng sớm mùa đông và đầu giờ chiều nắng gắt; áp dụng kiểm soát giờ xe tải nặng vào nội đô ban đêm. |\n"
                "| **5** | **Bằng chứng từ đợt phong tỏa COVID-19:** Khi đóng băng hoạt động kinh tế, NO2 giảm trung bình **35.4%** và PM2.5 giảm **30.7%** trên 19 thành phố đối chiếu. NO2 giảm mạnh hơn do phản ánh sự tê liệt của xe cơ giới (Ahmedabad NO2 giảm 66.5%, PM2.5 giảm 59.1%). Quan sát rõ các ngoại lệ Mumbai (+30.7% PM2.5) và Thiruvananthapuram. | **Chart 5** | Minh chứng chất lượng không khí hoàn toàn có thể cải thiện nhanh chóng nếu có chính sách quyết liệt hạn chế phát thải xe cơ giới và chuyển đổi giao thông xanh. |\n\n"
                "---\n\n"
                "### Giới hạn của dữ liệu & Định hướng tiếp theo (*Limitations & Next Steps - Section 6*):\n"
                "- **Giới hạn 1 (Độ phủ thành phố):** Dữ liệu tập trung ở 26 thành phố lớn, chưa bao gồm các đô thị cấp hai, thị trấn nông thôn nơi hoạt động đốt rác thải nông nghiệp và đun nấu sinh khối diễn ra phổ biến. Cần mở rộng mạng lưới quan trắc ra vùng ngoại vi.\n"
                "- **Giới hạn 2 (Thiếu dữ liệu khí tượng):** Tập dữ liệu chưa có các thông số nhiệt độ, độ ẩm, tốc độ gió và chiều cao tầng hòa trộn (*mixing layer height*). Việc thu thập bổ sung dữ liệu vi khí hậu là bước tiếp theo thiết yếu để xây dựng mô hình dự báo học máy (Machine Learning) chính xác."
            )
            c['source'] = [new_text]

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Successfully updated {nb_path}")

update_notebook('notebooks/04_eda.ipynb')
update_notebook('notebooks/main.ipynb')
