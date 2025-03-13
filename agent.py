from zswarm import Swarm, Agent
import streamlit as st
import os

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


client = Swarm()

def youtube_summarize(text):
    summerizer = Agent(
        name="Summarizer",
        model="gemini/gemini-2.0-pro-exp-02-05",
        instructions = """
Detailed content compilation with an objective tone and clear structure:
1.	Each section must begin with a numbered main heading, placed on a separate line.
2.	Directly below the main heading, key points must be listed on separate lines for readability.
3.	The content must be arranged logically, progressing from macro to micro levels to ensure clarity: 
- Macro level: International scope, global trends, and their impact on the world economy.
- Intermediate level: Global corporations, multinational enterprises, and the effects of international policies.
- Micro level: Domestic context, local businesses, and their influence on citizens and the national market.

*MUST Rules*:
- Preserve the original language of the passage without translating or reinterpreting.
- Only return the compiled content, excluding any introductions, conclusions, or external commentary.
- Do not add, modify, or infer any information not explicitly stated in the original text.
- Maintain an objective tone throughout, avoiding personal opinions or biases.
- If the passage contains a section answering audience questions, it must be included in full without omission or alteration.
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

