import streamlit as st
import time
from youtube_transcript_api import YouTubeTranscriptApi as yta
from agent import youtube_summarize
from config import AVAILABLE_LANGUAGES

# Function to fetch transcript with retry logic
def get_transcript_with_retry(video_id, lang, retries=10, delay=1):
    for attempt in range(retries):
        try:
            return yta.get_transcript(video_id, languages=[lang])
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def main():
    st.set_page_config(page_title="ClipSum", page_icon=":rocket:", layout="wide")  

    # Set sidebar title
    st.sidebar.title("ClipSum")
    
    # Initialize summary history in session state
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Display chat history using the first line of each summary
    st.sidebar.subheader("Chat History")
    if st.session_state["history"]:
        for summary in st.session_state["history"][-5:]:  # Show only the last 5 summaries
            first_line = summary.split("\n")[2].strip()  # Extract the first line
            if len(first_line) > 50:  # Truncate if it's too long
                first_line = first_line[:50] + "..."
            with st.sidebar.expander(f"🔹 {first_line}"):
                st.write(summary)

        # Button to clear history
        if st.sidebar.button("🗑️ Clear History"):
            st.session_state["history"] = []
            st.rerun()

    # Create a layout with two columns (75% - 25%)
    col1, col2 = st.columns([3, 1])

    # User input for YouTube URL
    with col1:
        youtube_url = st.text_input("Enter YouTube URL:")

    # Dropdown for selecting subtitle language
    with col2:
        selected_lang = st.selectbox("Choose subtitle language:", list(AVAILABLE_LANGUAGES.keys()))

    # Button to generate the summary
    if st.button("Summarize 🚀"):
        if youtube_url:
            try:
                # Validate the YouTube URL format
                if "v=" not in youtube_url:
                    st.error("⚠️ Invalid URL! Please enter a valid YouTube URL.")
                    return

                # Extract video ID from the URL
                video_id = youtube_url.split("v=")[1].split("&")[0]
                with st.spinner("🔍 Extracting subtitles and summarizing... This may take a moment!"):
                    # Fetch transcript from YouTube with retry logic
                    list_text = get_transcript_with_retry(video_id, AVAILABLE_LANGUAGES[selected_lang])
                    text = " ".join([d["text"] for d in list_text])
                    # Summarize using LLM
                    result = "\n\n" + youtube_summarize(text)
                
                print(result)
                # Display the summary after processing with a scrollable container with border
                st.success("✅ Summary is ready!")
                st.markdown(
                    f'<div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; height:400px; overflow-y: auto;">{result}</div>', 
                    unsafe_allow_html=True
                )

                # Save the summary to history
                st.session_state["history"].append(result)

            except Exception as e:
                st.error("⚠️ Cannot retrieve subtitles. Please check the language and try again.")
        else:
            st.error("⚠️ Please enter a YouTube URL.")

if __name__ == "__main__":
    main()
