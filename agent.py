import streamlit as st
from google import genai
from google.genai import types
import os

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def youtube_summarize(text):
    client = genai.Client(api_key=GEMINI_API_KEY)
    instructions = """
You are an helpful assistant.
Stricted Rules:
- *Preserve* the original language of the input text.
- *Must* return only the summarized content.
- *Do not* include introductory sentences or extra commentary.
- *Do not* add, modify, or infer any information not present in the original text.
- *Must* maintain an objective tone throughout.
"""
    prompt = f"""Hãy đọc đoạn văn và hiểu nó một cách rõ ràng. Sau đó tóm tắt thật chi tiết cho tôi đoạn văn với yêu cầu: Từ những vấn đề vĩ mô đên vi mô, Chia ra từng đoạn với các đầu mục chính, ý chính. Có nhấn mạnh ý chính của từng đoạn, Vấn đề nào quan trọng để thể tách riêng, Viết ngắn gọn nhưng vẫn đủ ý, Viết dễ hiểu.Đặc biệt là không được bịa, chỉ được lấy ý từ tác giả. Trong đoạn có thể xuất hiện các phần chính của tác giả thì có thể tóm tắt từ đó.
Nội dung cần tóm tắt: {text}
"""
    response = client.models.generate_content(
                model="gemini-2.0-flash-thinking-exp-01-21",
                config=types.GenerateContentConfig(
                    temperature=0,
                    top_p=0.95,
                    top_k=64,
                    max_output_tokens=100000,
                    response_mime_type="text/plain",
                    system_instruction=instructions),
                contents=[prompt]
            )  
    raw_text = response.candidates[0].content.parts[0].text
    result = raw_text.replace("```", "").replace("div", "").strip()
    return result

def youtube_summarize_ordered(text):
    client = genai.Client(api_key=GEMINI_API_KEY)
    instructions = """
You are an helpful assistant.
Stricted Rules:
- *Preserve* the original language of the input text.
- *Must* return only the summarized content.
- *Do not* include introductory sentences or extra commentary.
- *Do not* add, modify, or infer any information not present in the original text.
- *Must* maintain an objective tone throughout.
"""
    first_order = f"""
Hãy đọc đoạn văn và hiểu nó một cách rõ ràng. Sau đó tóm tắt thật chi tiết cho tôi đoạn văn với yêu cầu: Từ những vấn đề vĩ mô đên vi mô, Chia ra từng đoạn với các đầu mục chính, ý chính. Có nhấn mạnh ý chính của từng đoạn, Vấn đề nào quan trọng để thể tách riêng, Viết ngắn gọn nhưng vẫn đủ ý, Viết dễ hiểu.Đặc biệt là không được bịa, chỉ được lấy ý từ tác giả. Trong đoạn có thể xuất hiện các phần chính của tác giả thì có thể tóm tắt từ đó.
"""
    second_order = f"""
Hơn nữa, đoạn văn này là cuộc đối thoại giữa nhiều người với nhau. Cố gắng đọc thật kỹ và lọc ra lời thoại của từng người nhé. 
Nội dung cần tóm tắt dưới đây: 
{text}
"""
    response = client.models.generate_content(
                model="gemini-2.0-flash-thinking-exp-01-21",
                config=types.GenerateContentConfig(
                    temperature=0,
                    top_p=0.95,
                    top_k=64,
                    max_output_tokens=100000,
                    response_mime_type="text/plain",
                    system_instruction=instructions),
                contents=[first_order, second_order]
            )  
    raw_text = response.candidates[0].content.parts[0].text
    result = raw_text.replace("```", "").replace("div", "").strip()
    print(result)
    return result
