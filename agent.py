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
        instructions = """Summarize the following passage by structuring it into clearly defined sections. The summary **must** follow a two-level structure:  
        1. Each section **must** start with a **main heading**, placed on a separate line.  
        2. Directly below each **main heading**, the key ideas **must** be listed as bullet points (e.g., "- key idea").  

        Ensure the summary flows logically from a broad overview (macro) to detailed insights (micro) for better readability.  

        ### Rules:  
        - **Preserve** the original language of the input text.  
        - **Must** return only the summarized passage
        - **Do not** include introductory sentences or extra commentary.  
        - **Do not** add, modify, or infer any information not present in the original text.  
        - **Must** maintain an objective tone throughout.  
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
    return res
