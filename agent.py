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
        instructions = """Summarize the following passage by organizing it into clearly defined sections. For each section:
        1. Start with a main heading.
        2. Under each heading, list the key ideas as bullet points.

        Ensure the summary flows from a broad overview to detailed insights for better readability.

        Rules:
        - Return only the summarized passage—no introductory sentences or extra explanations.
        - Do not add, modify, or infer any information.
        - Maintain an objective tone.
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
    #res = res.replace("*", "")
    return res
