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
        instructions = """Summarize the following passage by breaking it into clear, distinct sections. For each section:
        1. Begin with a main heading.
        2. List the key points underneath as bullet points.
        
        Ensure the summary flows from a broad overview (macro) to detailed insights (micro) for enhanced readability.
        
        Rules:
        - Do not add, modify, or infer any information.
        - Maintain an objective tone.
        - Return only the summarized passage—no introductory sentences or extra explanations.
        - Preserve the original language of the input text.
        """,
        functions=[],
        model_config={
                "temperature": 0,
                }
    )

    response = client.run(
        agent=summerizer,
        messages=[{"role": "user", "content":  text}],
    )

    res = response.messages[-1]["content"]
    res = res.replace("*", "")
    return res
