import streamlit as st
import time
from youtube_transcript_api import YouTubeTranscriptApi as yta
from agent import youtube_summarize, youtube_summarize_ordered 
import os 
import base64
from PIL import Image

from config import AVAILABLE_LANGUAGES

def get_image_as_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def get_transcript_with_retry(video_id, lang, retries=5, delay=5):
    for attempt in range(retries):
        try:
            return yta.get_transcript(video_id, languages=[lang])
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def youtube_summarize_with_retry(text, retries=5, delay=5):
    for attempt in range(retries):
        try:
            return youtube_summarize(text)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def youtube_summarize_ordered_with_retry(text, retries=5, delay=5):  # New function for ordered summary
    for attempt in range(retries):
        try:
            return youtube_summarize_ordered(text)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def main():
    icon = Image.open("assets/ClipSum.jpg")
    st.set_page_config(page_title="ClipSum", page_icon=icon, layout="wide")

    # Header
    st.markdown("""
        <h1 style='text-align: center; font-size: 3em; font-weight: bold;'>CLIPSUM</h1>
    """, unsafe_allow_html=True)
    
    # Main layout
    youtube_url = st.text_input("Enter YouTube URL:")
    selected_lang = st.selectbox("Choose Subtitle Language:", list(AVAILABLE_LANGUAGES.keys()))
    
    # Sidebar layout
    with st.sidebar:
        logo_path = os.path.join("assets", "ClipSum.jpg")
        img_str = get_image_as_base64(logo_path)
        
        if img_str:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="data:image/jpeg;base64,{img_str}" alt="ClipSum Logo" width="250" 
                    style="border-radius: 15px; border: 4px solid #FFFFFF; box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.6);">
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("""<h3 style='text-align: center;'>AI-powered YouTube summarizer</h3>""", unsafe_allow_html=True)
        
        # Summary history section
        if "history" not in st.session_state:
            st.session_state["history"] = []

        st.sidebar.markdown("### Recent Summaries")

        if st.session_state["history"]:
            for summary in st.session_state["history"][-5:]:  # Display 5 most recent summaries
                first_line = summary.split("\n")[2].strip("#").strip() if len(summary.split("\n")) > 2 else summary[:50]
                if len(first_line) > 50:
                    first_line = first_line[:50].strip("#") + "..."
                
                # Each summary has its own expander
                with st.sidebar.expander(f"🔹 {first_line}"):
                    st.write(summary)

            # Clear history button
            if st.sidebar.button("🗑️ Clear History"):
                st.session_state["history"] = []
                st.rerun()
        else:
            st.sidebar.write("No summaries yet.")
    
    # Tabs at the bottom
    tab1, tab2, tab3 = st.tabs(["Transcript", "Summarize", "Summarize Ordered"])  # Added third tab
    
    with tab1:
        if st.button("Get Transcript 🚀"):
            if youtube_url:
                try:
                    if "v=" not in youtube_url:
                        st.error("⚠️ Invalid URL! Please enter a valid YouTube URL.")
                        return
                    video_id = youtube_url.split("v=")[1].split("&")[0]
                    with st.spinner("Extracting transcript..."):
                        list_text = get_transcript_with_retry(video_id, AVAILABLE_LANGUAGES[selected_lang])
                        transcript = "\n".join([d["text"] for d in list_text])
                        st.session_state["transcript"] = transcript
                    st.success("✅ Transcript fetched successfully!")
                    st.text_area("Transcript:", transcript, height=300)
                except Exception as e:
                    st.error("⚠️ Cannot retrieve subtitles. Please check the language and try again.")
            else:
                st.error("⚠️ Please enter a YouTube URL.")
    
    with tab2:
        if st.button("Summarize 🚀"):
            if youtube_url:
                try:
                    if "v=" not in youtube_url:
                        st.error("⚠️ Invalid URL! Please enter a valid YouTube URL.")
                        return
                    video_id = youtube_url.split("v=")[1].split("&")[0]
                    with st.spinner("Extracting subtitles and summarizing... This may take a moment!"):
                        if "transcript" in st.session_state:
                            text = st.session_state["transcript"]
                        else:
                            list_text = get_transcript_with_retry(video_id, AVAILABLE_LANGUAGES[selected_lang])
                            text = " ".join([d["text"] for d in list_text])
                        result = "\n\n" + youtube_summarize_with_retry(text)
                    
                    st.success("✅ Summary is ready!")
                    st.markdown(
                        f'<div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; height:400px; overflow-y: auto;">{result}</div>', 
                        unsafe_allow_html=True
                    )
                    st.session_state["history"].append(result)
                except Exception as e:
                    st.error("⚠️ Cannot retrieve subtitles. Please check the language and try again.")
            else:
                st.error("⚠️ Please enter a YouTube URL.")

    with tab3:  # New tab for ordered summary
        if st.button("Summarize Ordered 🚀"):
            if youtube_url:
                try:
                    if "v=" not in youtube_url:
                        st.error("⚠️ Invalid URL! Please enter a valid YouTube URL.")
                        return
                    video_id = youtube_url.split("v=")[1].split("&")[0]
                    with st.spinner("Extracting subtitles and summarizing (ordered)... This may take a moment!"):
                        if "transcript" in st.session_state:
                            text = st.session_state["transcript"]
                        else:
                            list_text = get_transcript_with_retry(video_id, AVAILABLE_LANGUAGES[selected_lang])
                            text = " ".join([d["text"] for d in list_text])
                        result = "\n\n" + youtube_summarize_ordered_with_retry(text)
                    st.success("✅ Ordered Summary is ready!")
                    st.markdown(
                        f'<div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; height:400px; overflow-y: auto;">{result}</div>', 
                        unsafe_allow_html=True
                    )
                    st.session_state["history"].append(result)
                except Exception as e:
                    st.error("⚠️ Cannot retrieve subtitles. Please check the language and try again.")
            else:
                st.error("⚠️ Please enter a YouTube URL.")

if __name__ == "__main__":
    main()
