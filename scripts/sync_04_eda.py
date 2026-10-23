import json
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

def sync_all():
    eda_path = 'notebooks/04_eda.ipynb'
    main_path = 'notebooks/main.ipynb'
    build_script_path = 'scripts/build_section_4.py'

    print(f"Reading {eda_path} and {main_path}...")
    with open(eda_path, 'r', encoding='utf-8') as f:
        eda_nb = json.load(f)
    with open(main_path, 'r', encoding='utf-8') as f:
        main_nb = json.load(f)

    # Text blocks with raw strings to preserve LaTeX backslashes (\rho, \text, etc.)
    cell5_text = (
        r"""### Diễn giải chi tiết trả lời 4 câu hỏi trong Slide 16:

1. **Location - *"what is typical?"***
   - Nồng độ trung vị điển hình của bụi mịn PM2.5 ở các thành phố là **48.41 µg/m³**, tiệm cận quy chuẩn 24h quốc gia của Ấn Độ (60 µg/m³) và **gấp 3.2 lần ngưỡng khuyến nghị của WHO 2021 (15 µg/m³)**.
   - AQI tính lại có mức trung vị là **115.29** (thuộc cấp *Moderate*). Tuy nhiên, giá trị trung bình Mean của AQI lên tới **161.86** và PM2.5 là **64.11 µg/m³**. Khoảng chênh lệch lớn giữa Mean và Median phản ánh rõ sự kéo lệch bởi các đợt ô nhiễm cực trị mùa đông.

2. **Spread - *"how consistent is it?"***
   - Bụi mịn PM2.5 có độ biến thiên rất cao với $IQR = 45.72$ µg/m³ và hệ số biến thiên $CV = 0.85$ (85%). AQI có khoảng tứ phân vị $IQR = 119.12$ và $CV = 0.78$.
   - Đặc biệt, khí CO có $CV = 2.53$ (253%) và $Range = 124.01$, thể hiện sự dao động nồng độ cực kỳ bất ổn định giữa các thành phố công nghiệp và các thành phố sinh thái.

3. **Shape - *"which summary is even valid here?"***
   - Toàn bộ các chất đều có **Skewness dương lớn ($\text{Skew} > 1.0$)**, đặc biệt là CO ($\text{Skew} = 7.53$) và AQI ($\text{Skew} = 2.81$). Hệ số Kurtosis đều vượt xa chuẩn ($\text{Kurt} > 3.0$, CO đạt 82.38 và AQI đạt 16.04), chứng minh dạng phân bố **Leptokurtic đuôi rất dày (heavy-tailed)**.
   - **Thước đo nào hợp lệ ở đây?** Do phân bố bị lệch phải nghiêm trọng bởi các đỉnh ô nhiễm cực đoan mùa đông, thước đo trung bình số học (**Mean**) và độ lệch chuẩn (**Std**) bị bóp méo nặng nề. Do đó, **Median và IQR là các thước đo trung tâm và độ biến thiên hợp lệ, chuẩn xác nhất** để đại diện cho chất lượng không khí.

4. **Relationship - *"what goes with what?"*** (Xem chi tiết bảng tương quan và hiệp phương sai bên dưới)"""
    )

    cell7_text = (
        r"""### Nhận xét Họ 4 (Relationship - *"what goes with what?"*):
- **Bụi mịn chi phối toàn diện AQI:** AQI có tương quan Spearman cực cao với **PM10 ($\rho = 0.88$)** và **PM2.5 ($\rho = 0.84$)**, tiếp theo là **CO ($\rho = 0.61$)** và **NO2 ($\rho = 0.48$)**. Điều này khẳng định bụi mịn là tác nhân chính chi phối toàn diện chất lượng không khí tại các đô thị Ấn Độ.
- **Quan hệ cùng nguồn phát thải:** Bụi mịn PM2.5 và PM10 đồng hành mật thiết ($\rho = 0.88$). Khí oxit nitơ từ khí thải giao thông và công nghiệp cũng tương quan rất cao: NO2–NOx ($\rho = 0.69$) và NO–NO2 ($\rho = 0.43$). Nhóm hydrocacbon Benzene–Toluene đạt $\rho = 0.75$.
- **Phản ứng quang hóa của Ozone:** Ozone (O3) có tương quan âm nhẹ với NO ($\rho = -0.05$). Đây là đặc tính quang hóa khí quyển: khí NO phát thải từ ống xả xe phản ứng trực tiếp tiêu thụ phân tử Ozone ở tầng sát mặt đất."""
    )

    cell12_text = (
        """**Nhận xét phân tích nhóm Thành phố:**
- **Ahmedabad và các đô thị đồng bằng sông Hằng là tâm điểm ô nhiễm:** Thành phố công nghiệp phía Tây **Ahmedabad** đứng đầu bảng với mức độ ô nhiễm kỷ lục (AQI trung bình 398.8, AQI trung vị 350.8, 87.1% ngày ở mức Poor trở lên). Kế tiếp là các đại đô thị đồng bằng sông Hằng phía Bắc gồm **Delhi (AQI trung vị 236.9, 60.8% ngày Poor trở lên)**, **Gurugram (203.8, 51.1% ngày Poor+)**, **Lucknow (191.6, 47.7% ngày Poor+)** và **Patna (167.8, 43.6% ngày Poor+)**.
- **Khu vực không khí trong lành:** Các thành phố ven biển Nam Ấn và vùng núi Đông Bắc như **Aizawl (AQI trung vị 27.0)**, **Shillong (46.4)**, **Thiruvananthapuram (66.1)**, **Coimbatore (73.5)** và **Amaravati (74.7)** có tỷ lệ ngày đạt chuẩn Good/Satisfactory vượt trên 86%–100%, hầu như không xuất hiện ngày ô nhiễm mức Poor.
- **Sự khác biệt giữa các siêu đô thị:** Dù có mật độ dân số và xe cộ khổng lồ, Mumbai (AQI trung vị 90.4) và Chennai (97.2) có chỉ số AQI thấp hơn Delhi tới **hơn 2.4 đến 2.6 lần** nhờ vị trí địa lý ven biển có gió biển thổi liên tục giúp khuếch tán chất ô nhiễm."""
    )

    cell18_text = (
        """**Nhận xét phân tích nhóm Mùa vụ:**
- **Mùa đông (Tháng 12 – Tháng 2) là thời kỳ đen tối nhất:** AQI trung vị toàn quốc lên tới **172.8** (trung bình là **220.8**), PM2.5 trung vị **74.0 µg/m³**, và **42.4% số ngày rơi vào mức Poor trở lên**.
- **Mùa mưa gió mùa (Tháng 6 – Tháng 9) là thời điểm trong lành nhất:** AQI trung vị giảm sâu xuống **90.4**, PM2.5 trung vị chỉ còn **33.1 µg/m³**, và tỷ lệ ngày Poor giảm chỉ còn **9.0%** nhờ nước mưa rửa trôi hạt bụi (*wet scavenging*).
- **Hệ số Mùa Đông / Mùa Mưa:** Mức chênh lệch lớn nhất cả nước không phải là Delhi mà thuộc về **Guwahati (gấp 6.17 lần - từ 46.3 mùa mưa lên 285.4 mùa đông)**, tiếp theo là **Kolkata (gấp 4.34 lần)**, **Patna (gấp 3.77 lần)**, **Lucknow (gấp 3.28 lần)**, và **Delhi (gấp 2.37 lần)**.
- **Cơ chế khí quyển:** Vào mùa đông, thời tiết lạnh kèm gió yếu gây ra hiện tượng **nghịch nhiệt tầng biên (*boundary layer inversion*)**, tạo thành một chiếc 'nắp nồi' nhiệt nhốt chặt toàn bộ khí thải giao thông và khói đốt rơm rạ sát mặt đất."""
    )

    cell21_text = (
        """**Nhận xét Hiệu ứng cuối tuần (*Weekend Effect*):**
- Mức sụt giảm nồng độ vào cuối tuần là **hầu như không đáng kể**: PM2.5 trung vị ngày thường là **48.49 µg/m³**, cuối tuần là **48.21 µg/m³** (chỉ giảm **0.58%**); PM10 trung vị giảm **1.06%**; NO2 trung vị giảm **3.05%**; và AQI trung vị hầu như không đổi (**115.11 so với 115.62**).
- **Ý nghĩa thực tế:** Các nguồn phát thải nền chủ yếu tại Ấn Độ (nhà máy nhiệt điện than liên vùng, đun nấu sinh hoạt bằng củi/than, và xe tải vận tải đường dài) hoạt động liên tục 7 ngày trong tuần. Ngoài ra, bụi mịn PM2.5 có thời gian lưu lơ lửng trong khí quyển từ 5 đến 7 ngày nên không thể suy giảm tức thì chỉ sau 1–2 ngày nghỉ cuối tuần."""
    )

    cell24_text = (
        """**Nhận xét Chu kỳ 24 giờ:**
- **Mẫu hình hai đỉnh của các chất phát thải sơ cấp (PM2.5, NO2, CO):**
  - Đỉnh sáng (**8h – 9h**): Giờ cao điểm phương tiện bắt đầu lưu thông (PM2.5 đạt 71.1 µg/m³, NO2 đạt 28.0 µg/m³).
  - Đỉnh đêm (**20h – 22h**): Nồng độ cao nhất trong ngày do xe tải nặng vào nội đô kết hợp lớp nghịch nhiệt ban đêm hạ thấp ép bụi xuống sát mặt đường (NO2 lúc 20h đạt 40.0 µg/m³ - cao hơn trung bình ngày **41%**; CO lúc 21h đạt 3.9 mg/m³ - cao hơn **69%**; PM2.5 lúc 22h-23h đạt 77.0 µg/m³ - cao hơn **20%**).
  - Đáy nồng độ (**15h – 17h**): Bức xạ mặt trời nung nóng mặt đất thúc đẩy đối lưu xáo trộn không khí theo chiều đứng (PM2.5 hạ xuống 49.1 µg/m³).
- **Pha ngược chiều hoàn toàn của Ozone (O3):**
  - Ozone chạm đáy lúc 7h sáng (**21.2 µg/m³**, chỉ số 0.62) và bùng phát đạt đỉnh cực đại lúc **14h–15h chiều (55.0 µg/m³, chỉ số 1.61 - tăng gấp 2.59 lần so với đáy)**. Đây là đặc tính của chất ô nhiễm thứ cấp hình thành từ phản ứng quang hóa khi có ánh nắng mặt trời gay gắt."""
    )

    cell27_text = (
        """> [!NOTE]
> **Nhận xét thận trọng theo năm:** Nồng độ PM2.5 trung vị duy trì mức cao ~44–60 µg/m³ giai đoạn 2015–2019 (2015: 54.5, 2016: 60.0, 2017: 53.2, 2018: 51.5, 2019: 44.3 µg/m³), sau đó giảm xuống **36.1 µg/m³** trong năm 2020. Tuy nhiên, năm 2020 chỉ có dữ liệu 6 tháng đầu năm (bao gồm đợt phong tỏa nghiêm ngặt COVID-19 và thiếu các tháng mùa đông ô nhiễm nhất cuối năm). Do đó, cần tránh ngộ nhận rằng không khí đã được cải thiện bền vững trong năm 2020."""
    )

    cell28_text = (
        """## 4.3. Năm biểu đồ then chốt (*Five Headline Charts - Rubric 20%*)

Các biểu đồ được xây dựng dựa trên bảng dữ liệu cấp thành phố `city_day` và `city_hour`, tuân thủ quy tắc đồ họa chuẩn mực và có **tiêu đề biểu đồ nêu rõ kết luận phân tích (*titles that state a conclusion*)**:

| # | Câu hỏi nghiên cứu | Dạng biểu đồ | Dữ liệu | Tiêu đề kết luận |
|---|-------------------|--------------|---------|------------------|
| **1** | Nồng độ AQI phân bố và chênh lệch ra sao giữa các vùng địa lý? | Horizontal Boxplot | `city_day` | *Ahmedabad và các đô thị Bắc Ấn (Delhi, Gurugram, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor/Very Poor; chênh lệch gấp 5–13 lần so với Nam Ấn và Đông Bắc* |
| **2** | Tỷ lệ số ngày người dân từng thành phố phải hít thở không khí độc hại là bao nhiêu? | 100% Stacked Bar | `city_day` | *Hơn 50%–87% số ngày tại Ahmedabad, Delhi, Gurugram ở mức kém (Poor) trở lên; trong khi Aizawl và Shillong có hơn 96%–100% ngày đạt chuẩn Good/Satisfactory* |
| **3** | Tính chu kỳ mùa vụ của bụi mịn PM2.5 diễn biến như thế nào tại từng thành phố? | Heatmap Month x City | `city_day` | *Ô nhiễm PM2.5 mang tính mùa vụ cực đoan: bùng phát đỉnh điểm vào mùa đông (T11–T1) và chạm đáy vào mùa mưa (T7–T8) — Vượt xa quy chuẩn 24h quốc gia (60 µg/m³)* |
| **4** | Chu kỳ 24 giờ của các chất biến thiên ra sao và khác biệt thế nào giữa các mùa? | Dual-Panel Line Chart | `city_hour` | *Khí thải giao thông và nghịch nhiệt ban đêm tạo 2 đỉnh ô nhiễm sáng (8–9h) và đêm (20–22h); Ozone đạt đỉnh trưa chiều (14–15h) do phản ứng quang hóa* |
| **5** | Đợt phong tỏa COVID-19 làm suy giảm nồng độ ô nhiễm cụ thể ra sao tại các thành phố? | Paired Bar Chart | `city_day` | *Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 35.4% và PM2.5 giảm 30.7% trên 19 thành phố có dữ liệu đối chiếu; các đại đô thị ghi nhận mức giảm sâu nhất* |"""
    )

    cell31_text = (
        """**Diễn giải Chart 1:**
- **Ahmedabad ở đỉnh bảng ô nhiễm:** Hộp tứ phân vị (IQR từ 25% đến 75%) của Ahmedabad nằm trọn vẹn từ 253.5 đến 483.7 với AQI trung vị lên tới **350.8** (mức Very Poor), và xuất hiện nhiều điểm ngoại lai chạm ngưỡng kịch khung 600 (Severe).
- **Nhóm đồng bằng sông Hằng Bắc Ấn ô nhiễm nghiêm trọng:** Delhi (AQI trung vị **236.9**, IQR 159.0–328.1), Gurugram (**203.8**), Lucknow (**191.6**) và Patna (**167.8**) đều có hộp IQR nằm sâu trong vùng Poor và Very Poor.
- **Phân cực địa lý sâu sắc so với miền Nam và Đông Bắc:** Các thành phố ở đáy biểu đồ như Aizawl (AQI trung vị **27.0**), Shillong (**46.4**), Thiruvananthapuram (**66.1**) và Coimbatore (**73.5**) có hộp IQR nằm gọn trong vùng an toàn Good và Satisfactory. Khoảng cách chênh lệch giữa đỉnh và đáy lên tới **13 lần**."""
    )

    cell34_text = (
        """**Diễn giải Chart 2:**
- **Gánh nặng ô nhiễm cực đoan tại Ahmedabad và Delhi:**
  + Tại Ahmedabad, có tới **87.1% số ngày trong năm** rơi vào mức ô nhiễm đáng báo động (trong đó Severe chiếm **39.6%**, Very Poor chiếm **25.6%**, Poor chiếm **21.9%**); số ngày người dân được hít thở không khí an toàn (Good/Satisfactory) chỉ vỏn vẹn **0.7%** (chưa đầy 3 ngày trong cả năm!).
  + Tại Delhi, có tới **60.8% số ngày** ở mức Poor trở lên (Poor 28.5%, Very Poor 23.9%, Severe 8.3%), trong khi tỷ lệ ngày đạt chuẩn an toàn (Good và Satisfactory) chỉ vỏn vẹn **5.4%** (chưa đầy 20 ngày/năm, hoàn toàn không có ngày nào đạt mức Good).
  + Các đô thị lân cận cũng chịu chung số phận: Gurugram có **51.1% ngày Poor+**, Lucknow **47.7%**, Patna **43.6%**.
- **Đối lập tuyệt đối ở nhóm sạch:** Aizawl đạt **100% số ngày an toàn** (Good chiếm 77.7%, Satisfactory 22.3%, hoàn toàn không có ngày nào vượt quá Satisfactory). Coimbatore đạt **96.3% ngày an toàn**, Shillong đạt **96.5%**.
- **Ý nghĩa y tế:** Bằng chứng cho thấy sự bất bình đẳng phơi nhiễm y tế tàn khốc — người dân tại Bắc Ấn và Ahmedabad phải hít thở không khí độc hại suốt hơn 2/3 thời gian của năm."""
    )

    cell37_text = (
        """**Diễn giải Chart 3:**
- **Hình thái chữ U đỏ rực mùa đông:** Nồng độ PM2.5 theo tháng bộc lộ hình chữ U rõ rệt: tăng vọt từ tháng 10, đạt đỉnh cực đại vào **tháng 11, tháng 12 và tháng 1**, sau đó giảm sâu vào mùa mưa **tháng 7, tháng 8 và tháng 9**.
- **Các kỷ lục nồng độ mùa đông:** Patna ghi nhận đỉnh điểm vào tháng 12 lên tới **241.5 µg/m³** (tháng 11 là 206.9 µg/m³); Delhi tháng 12 là **211.4 µg/m³** (tháng 11 là 204.6 µg/m³); Lucknow tháng 11 là **195.7 µg/m³** và tháng 12 là **194.0 µg/m³**; Gurugram tháng 12 là **161.4 µg/m³**.
- **Đối chiếu quy chuẩn:** Mức nồng độ này vượt từ **3 đến 4 lần quy chuẩn quốc gia 24h của Ấn Độ (60 µg/m³)** và gấp từ **13 đến 16 lần khuyến nghị của WHO (15 µg/m³)**.
- **Mùa mưa giải cứu không khí:** Vào tháng 7 và 8, nồng độ PM2.5 tại Delhi giảm xuống **44.9–49.6 µg/m³**, Patna còn **40.1–42.0 µg/m³**, Lucknow còn **35.7–36.1 µg/m³**, Kolkata giảm xuống **23.0 µg/m³** — mức chênh lệch giữa mùa đông và mùa mưa lên tới **5 đến 6 lần**."""
    )

    cell40_text = (
        """**Diễn giải Chart 4:**
- **Panel A (Mẫu hình theo giờ chuẩn hóa):**
  + Các chất phát thải sơ cấp (PM2.5, NO2, CO) có 2 đỉnh nhọn rõ rệt: Đỉnh sáng lúc **8h–9h** (giờ cao điểm giao thông) và đỉnh đêm muộn lúc **20h–22h**.
  + Đỉnh đêm muộn cao vượt trội do xe tải nặng vào nội đô kết hợp lớp nghịch nhiệt ban đêm ép bụi xuống mặt đất: NO2 lúc 20h tối cao hơn trung bình ngày tới **41%** (chỉ số 1.41); CO lúc 21h đêm cao hơn **69%** (chỉ số 1.69); PM2.5 lúc 22h–23h cao hơn **20%** (chỉ số 1.20).
  + Đáy nồng độ của bụi rơi vào **15h–17h** chiều khi đối lưu bốc cao khuếch tán chất ô nhiễm.
  + **Ozone (O3) hoàn toàn ngược pha:** Chạm đáy lúc 7h sáng (0.62) và tăng vọt đạt đỉnh vào **14h–15h chiều (1.61, cao hơn trung bình ngày 61%)** do phản ứng quang hóa khi có ánh nắng mặt trời gay gắt.
- **Panel B (Khác biệt mùa vụ):** Mẫu hình chu kỳ tồn tại ở cả 4 mùa, nhưng biên độ mùa đông vượt trội hoàn toàn: PM2.5 đêm mùa đông lên tới **120.7 µg/m³ (lúc 23h)** và sáng là 108.7 µg/m³; trong khi mùa mưa đường biểu đồ nằm bẹp ở đáy, cả ngày đêm chỉ dao động nhẹ từ **32.9 đến 41.8 µg/m³**, luôn an toàn dưới quy chuẩn 60 µg/m³."""
    )

    cell43_text = (
        """**Diễn giải Chart 5:**
- **Tổng thể trên 19 thành phố đối chiếu:** Giai đoạn phong tỏa toàn quốc nghiêm ngặt làm **NO2 giảm trung bình 35.4% và PM2.5 giảm 30.7%** so với cùng kỳ 2019.
- **NO2 sụt giảm sâu hơn PM2.5:** NO2 gắn liền với khí thải phương tiện giao thông nên khi lệnh cấm di chuyển có hiệu lực, nồng độ NO2 sụt giảm tức thì 50%–66% tại các thành phố lớn (Ahmedabad giảm **-66.5%**, Kolkata **-59.4%**, Amaravati **-55.8%**, Lucknow **-53.9%**, Jaipur **-51.4%**, Delhi **-46.5%**, Chennai **-45.1%**). PM2.5 giảm chậm hơn do vẫn còn nguồn phát thải nền từ các nhà máy điện than và nấu nướng sinh hoạt.
- **Nhận diện chính xác các ngoại lệ bên phải trục 0:**
  + Tại **Mumbai**, NO2 giảm -38.2% nhưng PM2.5 lại tăng **+30.7%** do các hoạt động công nghiệp cảng biển duy trì và điều kiện thời tiết khô hạn ven biển trong tháng 4-5/2020.
  + Tại **Thiruvananthapuram**, cột NO2 tăng **+93.3%** do năm 2019 trạm đo gián đoạn ít ngày, sang 2020 đo đầy đủ hơn kết hợp nguồn phát thải cục bộ gần vị trí đặt trạm."""
    )

    cell44_text = (
        r"""## 4.4. Tổng kết & Phát hiện then chốt (*Key Findings, Statistical Insights & Strategic Policy Implications*)

Mục 4.4 đóng vai trò đúc kết toàn diện các kết quả thu được từ phân tích khám phá dữ liệu (EDA) trên 29,531 bản ghi ngày (`city_day`) và 707,875 bản ghi giờ (`city_hour`) của 26 thành phố Ấn Độ (2015–2020), liên kết chặt chẽ giữa **4 họ số đo thống kê (Slide 16)**, **5 phân tích nhóm chuyên sâu**, và **5 biểu đồ then chốt (Headline Charts)**. Đây là cơ sở khoa học để phục vụ trực tiếp cho **Mục 5 (Key Findings)** và **Mục 6 (Limitations & Next Steps)** trong Báo cáo và Slide thuyết trình.

---

### 1. Bảng tổng hợp 5 phát hiện then chốt gắn liền với 5 Biểu đồ Headline Charts:

| # | Phát hiện then chốt (*Key Finding*) | Biểu đồ minh chứng | Ý nghĩa thực tiễn & Khuyến nghị chính sách (*Policy Implications*) |
|---|-------------------------------------|-------------------|-------------------------------------------------------------------|
| **1** | **Tâm điểm ô nhiễm cực đoan tại Ahmedabad và Đồng bằng sông Hằng:**<br>- **Ahmedabad** đứng đầu cả nước với mức độ ô nhiễm kỷ lục: AQI trung vị **350.8** (mức Very Poor), IQR trải rộng từ 253.5 đến 483.7, xuất hiện nhiều ngoại lai chạm ngưỡng kịch khung 600 (*Severe*).<br>- Kế tiếp là dải đô thị đồng bằng sông Hằng phía Bắc: **Delhi (AQI trung vị 236.9)**, **Gurugram (203.8)**, **Lucknow (191.6)**, và **Patna (167.8)**, toàn bộ hộp IQR đều nằm sâu trong vùng Poor và Very Poor.<br>- Chênh lệch từ **5 đến 13 lần** so với các đô thị ven biển Nam Ấn và vùng núi Đông Bắc (Aizawl 27.0, Shillong 46.4, Thiruvananthapuram 66.1). Dù dân số và xe cộ khổng lồ, Mumbai (90.4) và Chennai (97.2) sạch hơn Delhi 2.4–2.6 lần nhờ gió biển khuếch tán. | **Chart 1**<br>*(Horizontal Boxplot)* | **Quản lý chất lượng không khí theo lưu vực (*Airshed Management*):**<br>- Ô nhiễm không có biên giới hành chính; khói bụi bị giam hãm bởi địa hình bồn địa phía nam dãy Himalaya.<br>- Cần cơ chế điều phối liên bang quản lý chung toàn bộ lưu vực sông Hằng thay vì các biện pháp riêng lẻ, cục bộ của từng bang. |
| **2** | **Bất bình đẳng phơi nhiễm y tế tàn khốc giữa các vùng miền:**<br>- Người dân tại **Ahmedabad** phải chịu tới **87.1% số ngày trong năm** rơi vào mức ô nhiễm đáng báo động (trong đó **Severe chiếm 39.6%**, Very Poor 25.6%, Poor 21.9%); số ngày an toàn (Good/Satisfactory) chỉ vỏn vẹn **0.7%** (<3 ngày/năm).<br>- Tại **Delhi**, có **60.8% số ngày ở mức Poor trở lên** (Very Poor 23.9%, Severe 8.3%), số ngày an toàn chỉ vỏn vẹn **5.4%** (<20 ngày/năm, hoàn toàn không có ngày Good). Tương tự: Gurugram có 51.1% ngày Poor+, Lucknow 47.7%, Patna 43.6%.<br>- Đối lập tuyệt đối: **Aizawl đạt 100% ngày an toàn** (Good 77.7%, Satisfactory 22.3%), Coimbatore 96.3%, Shillong 96.5%. | **Chart 2**<br>*(100% Stacked Bar)* | **Ưu tiên y tế dự phòng & Công bằng môi trường (*Environmental Justice*):**<br>- Người dân miền Bắc và Ahmedabad phải phơi nhiễm không khí độc hại suốt hơn 2/3 thời gian của năm.<br>- Ưu tiên ngân sách y tế dự phòng, phát khẩu trang N95, lắp đặt hệ thống lọc khí tại tất cả trường học, bệnh viện và ban hành hướng dẫn cảnh báo hô hấp đặc biệt cho người già và trẻ nhỏ. |
| **3** | **Tính chu kỳ mùa vụ cực đoan — Bùng nổ mùa đông & Rửa trôi mùa mưa:**<br>- Bụi mịn PM2.5 biến thiên theo hình chữ U đỏ rực: bùng phát từ tháng 10, đạt đỉnh cực đại vào **tháng 11, 12 và tháng 1** (Patna tháng 12 đạt **241.5 µg/m³**, Delhi **211.4 µg/m³**, Lucknow **195.7 µg/m³**, Gurugram **161.4 µg/m³**).<br>- Mức này vượt từ **3 đến 4 lần quy chuẩn quốc gia 24h (60 µg/m³)** và gấp từ **13 đến 16 lần khuyến nghị WHO (15 µg/m³)**.<br>- Mùa mưa gió mùa (T7–T8), nồng độ giảm sâu xuống **23.0–49.6 µg/m³** nhờ cơ chế rửa trôi hạt bụi (*wet scavenging*). Hệ số chênh lệch đông/mưa lên tới **5–6 lần** tại các đại đô thị. | **Chart 3**<br>*(Heatmap Month x City)* | **Kích hoạt Kế hoạch Ứng phó Khẩn cấp Sớm (*Early Winter Action Plan*):**<br>- Hiện tượng **nghịch nhiệt tầng biên (*boundary layer inversion*)** vào mùa đông tạo chiếc "nắp nồi" nhốt chặt phát thải sát mặt đất.<br>- Kế hoạch hành động khẩn cấp (GRAP - cấm đốt rơm rạ, dừng thi công xây dựng hở, kiểm soát xe cũ) phải được tự động kích hoạt sớm từ **tháng 10**, không được đợi đến khi sương mù mù mịt vào tháng 12 mới ứng phó bị động. |
| **4** | **Quy luật phát thải 2 đỉnh giao thông sáng/đêm và pha quang hóa Ozone buổi trưa:**<br>- Các chất phát thải sơ cấp (PM2.5, NO2, CO) có 2 đỉnh nhọn: Đỉnh sáng (**8h–9h**) vào giờ cao điểm đi làm và Đỉnh đêm muộn (**20h–22h**). Đỉnh đêm cao vượt trội: NO2 lúc 20h cao hơn trung bình ngày **41%**, CO lúc 21h cao hơn **69%**, PM2.5 lúc 22h-23h cao hơn **20%** do xe tải diesel nặng vào nội đô kết hợp lớp nghịch nhiệt đêm hạ thấp.<br>- Đáy nồng độ bụi rơi vào **15h–17h** chiều khi đối lưu nhiệt xáo trộn thẳng đứng.<br>- **Ozone (O3) hoàn toàn ngược pha:** Chạm đáy lúc 7h sáng (21.2 µg/m³) và tăng vọt đạt đỉnh lúc **14h–15h (55.0 µg/m³, cao hơn trung bình ngày 61%, tăng 2.59 lần so với đáy)** do phản ứng quang hóa khi có nắng gắt. Ban đêm mùa đông, PM2.5 lên tới **120.7 µg/m³**.<br>- **Ý nghĩa sinh hoạt:** Nồng độ ô nhiễm biến thiên rất mạnh theo từng khung giờ trong ngày, đòi hỏi các cảnh báo sức khỏe chi tiết theo giờ. | **Chart 4**<br>*(Dual-Panel Line Chart)* | **Điều tiết giao thông thông minh & Hướng dẫn sinh hoạt theo giờ:**<br>- Cấm triệt để hoặc thu phí khí thải cao đối với xe tải nặng diesel đi xuyên tâm nội đô ban đêm (20h–23h), chuyển hướng sang các tuyến vành đai ngoài.<br>- Khuyến cáo người dân và người cao tuổi: **Tránh tập thể dục ngoài trời vào sáng sớm mùa đông** (nồng độ bụi và khí độc đậm đặc nhất) và **hạn chế hoạt động ngoài trời lúc 13h–15h trưa nắng gắt** (thời điểm nồng độ Ozone oxy hóa gây viêm đường thở cao nhất). |
| **5** | **Bằng chứng thực nghiệm từ phong tỏa COVID-19 (Thiên nhiên tự chữa lành):**<br>- Đợt phong tỏa toàn quốc nghiêm ngặt (25/3–03/5/2020) đóng băng giao thông và công nghiệp, làm **NO2 giảm trung bình 35.4%** và **PM2.5 giảm 30.7%** trên 19 thành phố đối chiếu.<br>- NO2 giảm sâu và nhanh hơn PM2.5 (Ahmedabad giảm **-66.5%**, Kolkata **-59.4%**, Amaravati **-55.8%**, Lucknow **-53.9%**, Delhi **-46.5%**) do phản ánh sự tê liệt tức thì của xe cơ giới; PM2.5 giảm chậm hơn do phát thải nền từ nhiệt điện than và sinh khối.<br>- Nhận diện rõ các ngoại lệ: **Mumbai** NO2 giảm -38.2% nhưng PM2.5 tăng **+30.7%** (do cảng biển hoạt động và khí hậu khô ven biển); **Thiruvananthapuram** NO2 tăng **+93.3%** do trạm đo 2019 ngắt quãng, 2020 đo đầy đủ hơn kết hợp nguồn cục bộ. | **Chart 5**<br>*(Paired Bar Chart)* | **Chuyển đổi giao thông xanh & Khẳng định tiềm năng đảo ngược ô nhiễm:**<br>- Bằng chứng thực nghiệm vô giá chứng minh: Không khí đô thị hoàn toàn có thể trong lành nhanh chóng nếu có chính sách quyết liệt hạn chế phát thải từ xe cơ giới.<br>- Khuyến nghị chính sách: Đẩy mạnh điện hóa 100% xe buýt công cộng, mở rộng mạng lưới Metro ngầm, nâng chuẩn khí thải BS-VI và loại bỏ xe thương mại quá niên hạn. |

---

### 2. Bốn Phát hiện Bổ sung Sâu sắc từ Phân tích Nhóm & Tương quan (Section 4.1 & 4.2):

1. **Bản chất phân phối Lệch phải nặng & Tính tất yếu của Thống kê Phi tham số (Section 4.1):**
   - Toàn bộ các chất ô nhiễm đều có độ lệch phải rất lớn ($\text{Skewness}_{\text{AQI}} = 2.81$, $\text{Skewness}_{\text{CO}} = 7.53$) và độ nhọn đuôi dày vượt chuẩn ($\text{Kurtosis}_{\text{CO}} = 82.38$, $\text{Kurtosis}_{\text{AQI}} = 16.04$).
   - Sự chênh lệch lớn giữa Mean và Median (AQI Mean 161.86 so với Median 115.29) khẳng định giá trị trung bình bị bóp méo nặng nề bởi các giá trị ngoại lai cực đoan mùa đông. **Median và IQR là các thước đo khoa học duy nhất hợp lệ, có tính kháng nhiễu (*robust statistics*)** phản ánh chuẩn xác chất lượng không khí đại diện.
   - Bụi hạt là nhân tố chi phối độc tôn: Tương quan Spearman của AQI với **PM10 đạt $\rho = 0.88$** và **PM2.5 đạt $\rho = 0.84$**.

2. **Sự vắng bóng của "Hiệu ứng Cuối tuần" (*Absence of Weekend Effect* - Section 4.2.3):**
   - Khác biệt chất lượng không khí giữa ngày làm việc (Thứ 2–Thứ 6) và cuối tuần (Thứ 7–Chủ Nhật) là **hầu như bằng 0**: PM2.5 trung vị chỉ giảm nhẹ **0.58%** (từ 48.49 xuống 48.21 µg/m³), PM10 giảm **1.06%**, NO2 giảm **3.05%**, và AQI trung vị hầu như không đổi (**115.11 so với 115.62, lệch +0.44%**).
   - *Nguyên nhân cốt lõi*: Các nguồn phát thải nền chủ lực (nhà máy nhiệt điện than liên vùng, đun nấu sinh hoạt bằng củi/than, xe vận tải đường dài) hoạt động liên tục 24/7 không nghỉ cuối tuần; kết hợp với **thời gian lưu lơ lửng của hạt PM2.5 trong khí quyển kéo dài từ 5 đến 7 ngày**, khiến ô nhiễm không thể tự tiêu tán chỉ sau 1–2 ngày nghỉ làm.

3. **Mức độ Nhạy cảm Mùa vụ Cực đoan theo từng Vùng Địa lý (*Seasonal Volatility* - Section 4.2.2):**
   - Hệ số bùng nổ ô nhiễm Mùa Đông / Mùa Mưa cao nhất cả nước không phải Delhi (gấp 2.37 lần) mà thuộc về **Guwahati (gấp 6.17 lần: từ 46.3 mùa mưa lên 285.4 mùa đông)**, tiếp theo là **Kolkata (gấp 4.34 lần: 59.8 lên 259.5)**, **Patna (gấp 3.77 lần: 94.2 lên 354.9)** và **Lucknow (gấp 3.28 lần)**.
   - Thung lũng sông và bồn địa Đông Bắc/Đông Ấn là những nơi chịu bẫy nghịch nhiệt mùa đông nặng nề nhất, cần cơ chế kiểm soát rơm rạ và sưởi ấm sinh khối khẩn cấp.

4. **Cảnh báo về Ngộ nhận Dữ liệu theo Năm (*Yearly Evolution Caution* - Section 4.2.5):**
   - Nồng độ PM2.5 trung vị duy trì mức cao ~44–60 µg/m³ giai đoạn 2015–2019, sau đó hạ xuống **36.1 µg/m³** trong năm 2020.
   - Cần cảnh báo thận trọng: Con số năm 2020 chỉ ghi nhận 6 tháng đầu năm (chứa đợt phong tỏa nghiêm ngặt COVID-19 và hoàn toàn vắng bóng 3 tháng mùa đông ô nhiễm nhất T10–T12). Do đó, sự sụt giảm này là **biến cố ngoại sinh tạm thời, tuyệt đối không được ngộ nhận là chất lượng không khí đã cải thiện bền vững**.

---

### 3. Giới hạn của Dữ liệu & Định hướng Tiếp theo sang Mô hình Machine Learning (*Limitations & Next Steps — Section 5 & 6*):

- **Giới hạn 1 (Độ bao phủ không gian - Spatial Coverage):** Dữ liệu tập trung ở 26 đô thị lớn với mạng lưới trạm đo nội đô, chưa bao quát được các đô thị cấp hai và dải nông thôn rộng lớn nơi tập trung hoạt động đốt sinh khối ngoài trời. Cần bổ sung dữ liệu viễn thám vệ tinh (AOD - Aerosol Optical Depth) để mở rộng độ phủ.
- **Giới hạn 2 (Thiếu các biến thời tiết vi khí hậu - Meteorological Drivers):** Bộ dữ liệu hiện tại chỉ gồm nồng độ các chất hóa học, hoàn toàn thiếu các thông số khí tượng then chốt như nhiệt độ, độ ẩm tương đối, tốc độ/hướng gió và chiều cao tầng hòa trộn khí quyển (*planetary boundary layer height*).
- **Giới hạn 3 (Tính liên tục của trạm đo & dữ liệu khuyết):** Dữ liệu năm 2020 kết thúc vào ngày 01/07/2020; một số thành phố (Kochi, Ernakulam, Aizawl) chỉ có chuỗi quan sát ngắn vài tháng.
- **Cầu nối Chiến lược sang Phần 5 (Feature Engineering & Machine Learning):**
  + Tận dụng các phát hiện EDA ở trên để kiến trúc các đặc trưng kỹ thuật (*Feature Engineering*):
    - **Đặc trưng độ trễ thời gian (Lag features):** Tạo các biến trễ $t-1$, $t-2$, $t-24$ giờ và $t-7$ ngày phản ánh tính quán tính và thời gian lưu khí quyển của PM2.5.
    - **Đặc trưng chu kỳ thời gian (Cyclical Encoding):** Áp dụng biến đổi hàm lượng giác $(\sin, \cos)$ cho Giờ trong ngày (chu kỳ 24h) và Tháng trong năm (chu kỳ 12 tháng) để mô hình học máy nắm bắt được quy luật 2 đỉnh giao thông và hình thái chữ U mùa đông.
    - **Đặc trưng thống kê trượt (Rolling Statistics):** Tính trung bình trượt và độ lệch chuẩn trượt (rolling mean/std 6h, 24h) để làm mượt nhiễu đo lường.
  + Đưa toàn bộ đặc trưng vào huấn luyện các mô hình học máy hồi quy (Linear Regression, Random Forest, Gradient Boosting, XGBoost/LightGBM) nhằm **dự báo chính xác nồng độ AQI và phân loại rủi ro sức khỏe kịp thời**."""
    )

    # Function to update a notebook object
    def update_nb_cells(nb):
        for i, c in enumerate(nb['cells']):
            txt = ''.join(c.get('source', []))
            if 'Diễn giải chi tiết trả lời 4 câu hỏi trong Slide 16:' in txt:
                c['source'] = [cell5_text]
            elif '### Nhận xét Họ 4 (Relationship' in txt:
                c['source'] = [cell7_text]
            elif '**Nhận xét phân tích nhóm Thành phố:**' in txt:
                c['source'] = [cell12_text]
            elif '**Nhận xét phân tích nhóm Mùa vụ:**' in txt:
                c['source'] = [cell18_text]
            elif '**Nhận xét Hiệu ứng cuối tuần' in txt:
                c['source'] = [cell21_text]
            elif '**Nhận xét Chu kỳ 24 giờ:**' in txt:
                c['source'] = [cell24_text]
            elif '**Nhận xét thận trọng theo năm:**' in txt:
                c['source'] = [cell27_text]
            elif '## 4.3. Năm biểu đồ then chốt' in txt:
                c['source'] = [cell28_text]
            elif '**Diễn giải Chart 1:**' in txt:
                c['source'] = [cell31_text]
            elif '**Diễn giải Chart 2:**' in txt:
                c['source'] = [cell34_text]
            elif '**Diễn giải Chart 3:**' in txt:
                c['source'] = [cell37_text]
            elif '**Diễn giải Chart 4:**' in txt:
                c['source'] = [cell40_text]
            elif '**Diễn giải Chart 5:**' in txt:
                c['source'] = [cell43_text]
            elif '## 4.4. Tổng kết & Phát hiện then chốt' in txt:
                c['source'] = [cell44_text]

            # Code title replacements
            elif 'chart1_title =' in txt:
                new_title_block = (
                    'chart1_title = (\n'
                    '    "Chart 1. Ahmedabad và các đô thị Bắc Ấn (Delhi, Gurugram, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor;\\n"\n'
                    '    "chênh lệch gấp 5–13 lần so với Nam Ấn và Đông Bắc"\n'
                    ')'
                )
                c['source'] = [re.sub(r'chart1_title = \([^)]+\)', new_title_block, txt)]

            elif 'chart2_title =' in txt:
                new_title_block = (
                    'chart2_title = (\n'
                    '    "Chart 2. Hơn 50%–87% số ngày tại Ahmedabad, Delhi, Gurugram ở mức kém (Poor) trở lên;\\n"\n'
                    '    "trong khi Aizawl và Shillong có hơn 96%–100% ngày đạt chuẩn Good/Satisfactory"\n'
                    ')'
                )
                c['source'] = [re.sub(r'chart2_title = \([^)]+\)', new_title_block, txt)]

            elif 'chart4_suptitle =' in txt:
                new_title_block = (
                    'chart4_suptitle = (\n'
                    '    "Chart 4. Khí thải giao thông và nghịch nhiệt ban đêm tạo 2 đỉnh ô nhiễm sáng (8–9h) và đêm (20–22h);\\n"\n'
                    '    "Ozone đạt đỉnh trưa chiều (14–15h) do phản ứng quang hóa"\n'
                    ')'
                )
                c['source'] = [re.sub(r'chart4_suptitle = \([^)]+\)', new_title_block, txt)]

            elif 'chart5_title =' in txt:
                new_title_block = (
                    'chart5_title = (\n'
                    '    "Chart 5. Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 35% và PM2.5 giảm 31% trên 19 thành phố có dữ liệu đối chiếu;\\n"\n'
                    '    "các đại đô thị (Ahmedabad, Kolkata, Lucknow, Delhi) ghi nhận mức giảm sâu nhất"\n'
                    ')'
                )
                c['source'] = [re.sub(r'chart5_title = \([^)]+\)', new_title_block, txt)]

    print("Updating 04_eda.ipynb...")
    update_nb_cells(eda_nb)
    with open(eda_path, 'w', encoding='utf-8') as f:
        json.dump(eda_nb, f, indent=1, ensure_ascii=False)
    print("Done 04_eda.ipynb.")

    print("Updating main.ipynb...")
    update_nb_cells(main_nb)
    with open(main_path, 'w', encoding='utf-8') as f:
        json.dump(main_nb, f, indent=1, ensure_ascii=False)
    print("Done main.ipynb.")

    # Also update build_section_4.py so that build script won't have stale data
    print(f"Updating {build_script_path}...")
    with open(build_script_path, 'r', encoding='utf-8') as f:
        build_code = f.read()

    # Replacements in build_section_4.py
    build_code = build_code.replace(
        "Delhi (AQI trung vị 213.3, 53% ngày Poor trở lên)",
        "Delhi (AQI trung vị 236.9, 60.8% ngày Poor trở lên)"
    )
    build_code = build_code.replace(
        "Thành phố Bắc Ấn (Delhi, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor;\\n\"\n    \"chênh lệch gấp 3–8 lần so với Nam Ấn và Đông Bắc",
        "Ahmedabad và các đô thị Bắc Ấn (Delhi, Gurugram, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor;\\n\"\n    \"chênh lệch gấp 5–13 lần so với Nam Ấn và Đông Bắc"
    )
    build_code = build_code.replace(
        "Thành phố Bắc Ấn (Delhi, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor; chênh lệch gấp 3–8 lần so với Nam Ấn và Đông Bắc",
        "Ahmedabad và các đô thị Bắc Ấn (Delhi, Gurugram, Lucknow, Patna) ô nhiễm nghiêm trọng, trung vị AQI vượt ngưỡng Poor/Very Poor; chênh lệch gấp 5–13 lần so với Nam Ấn và Đông Bắc"
    )
    build_code = build_code.replace(
        "Hơn 50% số ngày tại Delhi, Lucknow, Gurugram ở mức kém (Poor) trở lên;\\n\"\n    \"trong khi Aizawl và Shillong có hơn 98% ngày đạt chuẩn Good/Satisfactory",
        "Hơn 50%–87% số ngày tại Ahmedabad, Delhi, Gurugram ở mức kém (Poor) trở lên;\\n\"\n    \"trong khi Aizawl và Shillong có hơn 96%–100% ngày đạt chuẩn Good/Satisfactory"
    )
    build_code = build_code.replace(
        "Hơn 50% số ngày tại Delhi, Lucknow, Gurugram ở mức kém (Poor) trở lên; trong khi Aizawl và Shillong có hơn 98% ngày đạt chuẩn Good/Satisfactory",
        "Hơn 50%–87% số ngày tại Ahmedabad, Delhi, Gurugram ở mức kém (Poor) trở lên; trong khi Aizawl và Shillong có hơn 96%–100% ngày đạt chuẩn Good/Satisfactory"
    )
    build_code = build_code.replace(
        "- Tại Delhi, chỉ có **13% số ngày trong năm** đạt chuẩn an toàn, trong khi có tới **53% số ngày** rơi vào mức Poor trở lên (Very Poor chiếm 23%, Severe chiếm 9%).\n- Ngược lại, Aizawl đạt 99% ngày Good; Shillong đạt 98% Good/Satisfactory. Người dân tại vùng đồng bằng Bắc Ấn phải chịu rủi ro phơi nhiễm không khí độc hại cao gấp hàng chục lần so với vùng Đông Bắc.",
        """- **Gánh nặng ô nhiễm cực đoan tại Ahmedabad và Delhi:**
  + Tại Ahmedabad, có tới **87.1% số ngày trong năm** rơi vào mức ô nhiễm đáng báo động (trong đó Severe chiếm **39.6%**, Very Poor chiếm **25.6%**, Poor chiếm **21.9%**); số ngày người dân được hít thở không khí an toàn (Good/Satisfactory) chỉ vỏn vẹn **0.7%** (chưa đầy 3 ngày trong cả năm!).
  + Tại Delhi, có tới **60.8% số ngày** ở mức Poor trở lên (Poor 28.5%, Very Poor 23.9%, Severe 8.3%), trong khi tỷ lệ ngày đạt chuẩn an toàn (Good và Satisfactory) chỉ vỏn vẹn **5.4%** (chưa đầy 20 ngày/năm, hoàn toàn không có ngày nào đạt mức Good).
  + Các đô thị lân cận cũng chịu chung số phận: Gurugram có **51.1% ngày Poor+**, Lucknow **47.7%**, Patna **43.6%**.
- **Đối lập tuyệt đối ở nhóm sạch:** Aizawl đạt **100% số ngày an toàn** (Good chiếm 77.7%, Satisfactory 22.3%, hoàn toàn không có ngày nào vượt quá Satisfactory). Coimbatore đạt **96.3% ngày an toàn**, Shillong đạt **96.5%**.
- **Ý nghĩa y tế:** Bằng chứng cho thấy sự bất bình đẳng phơi nhiễm y tế tàn khốc — người dân tại Bắc Ấn và Ahmedabad phải hít thở không khí độc hại suốt hơn 2/3 thời gian của năm."""
    )
    build_code = build_code.replace(
        "Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 41% và PM2.5 giảm 34% trên 19 thành phố có dữ liệu đối chiếu;\\n\"\n    \"các đại đô thị (Ahmedabad, Kolkata, Lucknow, Delhi) ghi nhận mức giảm sâu nhất",
        "Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 35% và PM2.5 giảm 31% trên 19 thành phố có dữ liệu đối chiếu;\\n\"\n    \"các đại đô thị (Ahmedabad, Kolkata, Lucknow, Delhi) ghi nhận mức giảm sâu nhất"
    )
    build_code = build_code.replace(
        "Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 41% và PM2.5 giảm 34% trên 19 thành phố có dữ liệu đối chiếu; các đại đô thị ghi nhận mức giảm sâu nhất",
        "Đợt phong tỏa COVID-19 làm NO2 giảm mạnh 35.4% và PM2.5 giảm 30.7% trên 19 thành phố có dữ liệu đối chiếu; các đại đô thị ghi nhận mức giảm sâu nhất"
    )
    build_code = build_code.replace(
        "Người dân tại Delhi phải chịu hơn **53% số ngày trong năm** với không khí ở mức Poor trở lên (trong đó 32% là Very Poor và Severe); ngược lại Aizawl và Shillong có hơn **98% ngày đạt chuẩn Good/Satisfactory**.",
        "Người dân tại Ahmedabad và Delhi phải chịu từ **61% đến 87% số ngày trong năm** với không khí ở mức Poor trở lên (trong đó Ahmedabad có 39.6% ngày Severe); ngược lại Aizawl có **100% ngày đạt chuẩn an toàn** (Good/Satisfactory)."
    )
    build_code = build_code.replace(
        "**Bắc Ấn là tâm điểm ô nhiễm:** Các đô thị đồng bằng sông Hằng (Delhi, Lucknow, Gurugram, Patna) có trung vị AQI vượt ngưỡng Poor (155–213), cao gấp **3–8 lần** các đô thị ven biển Nam Ấn và đồi núi Đông Bắc.",
        "**Ahmedabad và Bắc Ấn là tâm điểm ô nhiễm:** Ahmedabad dẫn đầu cả nước (AQI trung vị 350.8), tiếp theo là các đô thị đồng bằng sông Hằng (Delhi 236.9, Gurugram 203.8, Lucknow 191.6, Patna 167.8), cao gấp **5–13 lần** các đô thị ven biển Nam Ấn và đồi núi Đông Bắc."
    )
    build_code = build_code.replace(
        "Khi đóng băng hoạt động kinh tế, NO2 giảm tới **41%** và PM2.5 giảm **34%** trên 19 thành phố đối chiếu. NO2 giảm mạnh hơn do phản ánh sự tê liệt của giao thông cơ giới.",
        "Khi đóng băng hoạt động kinh tế, NO2 giảm trung bình **35.4%** và PM2.5 giảm **30.7%** trên 19 thành phố đối chiếu. NO2 giảm mạnh hơn do phản ánh sự tê liệt của xe cơ giới (Ahmedabad NO2 giảm 66.5%, PM2.5 giảm 59.1%). Quan sát rõ các ngoại lệ Mumbai (+30.7% PM2.5) và Thiruvananthapuram."
    )

    # Replace section 4.4 in build_section_4.py with cell44_text
    build_code = re.sub(
        r'(# 4\.4 Tổng kết Key Findings\s*# =+\s*cells\.append\(md\()""".*?"""\)\)',
        lambda m: m.group(1) + 'r"""\n' + cell44_text + '\n"""\n    ))',
        build_code,
        flags=re.DOTALL
    )

    with open(build_script_path, 'w', encoding='utf-8') as f:
        f.write(build_code)
    print("Done build_section_4.py.")

if __name__ == '__main__':
    sync_all()
