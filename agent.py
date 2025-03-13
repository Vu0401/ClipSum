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
Extract detailed information from the passage with an *objective tone*, ensuring a structured and logical flow:
1.	Each section must begin with a *numbered main heading*, placed on a separate line.
2.	Directly below each main heading, key ideas must be listed as bullet points.

The content must be arranged logically, progressing from a broad perspective (macro) to more specific details (micro) for better clarity and comprehension.
Rules:
•	*Preserve* the original language of the input text.
•	*Only* return the extracted content, without any introductions, conclusions, or additional commentary.
•	*Do not* alter, add, or infer any information not explicitly present in the original text.
•	*Maintain* an objective tone throughout.
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

