from zswarm import Swarm, Agent
import streamlit as st
import os

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY


client = Swarm()



