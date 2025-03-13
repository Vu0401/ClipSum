from zswarm import Swarm, Agent
import streamlit as st
import os

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


client = Swarm()

def youtube_summarize(text):
    summerizer = Agent(
        name="Summarizer",
        model="gemini/gemini-2.0-flash-thinking-exp-01-21",
        instructions = """
**Tổng hợp nội dung một cách chi tiết với giọng văn khách quan và cấu trúc rõ ràng:**
1. Mỗi phần phải bắt đầu bằng một tiêu đề chính có đánh số, đặt trên một dòng riêng.
2. Ngay dưới tiêu đề chính, các ý quan trọng phải được liệt kê thành từng dòng riêng biệt để dễ đọc.
3. Nội dung phải được sắp xếp theo trình tự hợp lý, từ tổng quan đến chi tiết, đảm bảo sự logic: 
- Vĩ mô: Cấp độ quốc tế, các xu hướng toàn cầu, tác động đến nền kinh tế thế giới.
- Trung gian: Doanh nghiệp quốc tế, tập đoàn lớn, ảnh hưởng của các chính sách toàn cầu.
- Vi mô: Tình hình trong nước, doanh nghiệp nội địa, tác động đến người dân và thị trường trong nước.

**Quy tắc bắt buộc:**
- Giữ nguyên ngôn ngữ gốc của đoạn văn, không dịch hoặc diễn giải lại bằng ngôn ngữ khác.
- Chỉ trả về nội dung tổng hợp, không thêm phần mở đầu, kết luận hay bất kỳ bình luận nào bên ngoài nội dung gốc.
- Không thêm, bịa đặt hoặc suy diễn bất kỳ thông tin nào không có trong đoạn văn gốc.
- Giữ giọng văn khách quan xuyên suốt, không đưa cảm xúc cá nhân vào nội dung.
- Nếu đoạn văn có phần trả lời câu hỏi của người xem, phần đó phải được đưa vào đầy đủ mà không bị lược bỏ hoặc thay đổi ý nghĩa.
""",
        functions=[],
        model_config={
                "temperature": 0,
                "max_tokens": 500000,
                }
    )

    response = client.run(
        agent=summerizer,
        messages=[{"role": "user", "content":  text}],
    )

    res = response.messages[-1]["content"].replace("`", "").replace("div", "").strip()
    return res

