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
        instructions = """Please help me summarize the following passage logically. 
        Summarize the content by dividing it into clear sections, each starting with a numbered main heading followed by bullet points.
        The sections should progress from a macro to a micro perspective.
        Present the information from an overview to details for better readability. Do not add, modify, or infer any information. 
        Important: Maintain an objective tone and **must not** return any introductory sentences—only the summarized passage itself without any explanations. 
        Note: Keep the original language of the input text. 
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