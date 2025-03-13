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
        instructions = """Tóm tắt thật chi tiết và đầy đủ trình bày dài nhưng dễ nhìn.""",
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

