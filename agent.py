from zswarm import Swarm, Agent
import streamlit as st
import os

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


client = Swarm()

def youtube_summarize(text):
    summerizer = Agent(
        name="Summarizer",
        model="gemini/gemini-2.0-flash",
        instructions = """Transform the following passage into a well-structured, high-clarity summary with a **strict two-tier hierarchy**:

        1. **Section Headings**: Each section **must** start with a clearly distinguishable, bolded heading on a separate line.
        2. **Key Insights**: Under each heading, distill the essential points into concise bullet points (e.g., "- key idea"), ensuring readability and logical progression.
        
        ### Critical Constraints:
        - **No extraneous text**: The output **must** contain only the structured summary—no introductions, conclusions, or commentary.
        - **No interpretation**: Refrain from adding, altering, or assuming any information not explicitly stated in the original text.
        - **Preserve fidelity**: Maintain the original language and an objective, neutral tone throughout.
        
        ### Optimization Directives:
        - Structure the summary **from macro to micro**, ensuring a logical flow of ideas.
        - Format the output for **maximum skimmability**, making it easy to grasp key insights at a glance.
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
