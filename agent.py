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
Tổng hợp lại nội dung một cách chi tiết với giọng văn khách quan, có cấu trúc rõ ràng:
1.	Mỗi phần phải bắt đầu bằng một tiêu đề chính (đánh số), đặt trên một dòng riêng.
2.	Ngay dưới tiêu đề chính, các ý quan trọng phải được liệt kê thành từng dòng.
Đảm bảo nội dung được trình bày theo trình tự hợp lý, từ tổng quan (vĩ mô, quốc tế, doanh nghiệp quốc tế thế giới) đến chi tiết (vi mô, nội địa, doanh nghiệp trong nước) để dễ đọc và hiểu.
Quy tắc:
- Giữ nguyên ngôn ngữ gốc của đoạn văn.
- Chỉ trả về nội dung tổng hợp, không thêm lời dẫn hay bình luận.
- Không tự ý thêm, sửa đổi hay suy diễn nội dung không có trong đoạn gốc.
- Giữ giọng văn khách quan xuyên suốt.
- Nếu đoạn văn có phần trả lời câu hỏi của người xem, phần đó phải được đưa vào nội dung.
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

