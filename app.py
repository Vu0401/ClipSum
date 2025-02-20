import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi as yta
from agent import youtube_summarize
from config import AVAILABLE_LANGUAGES  

def main():
    st.set_page_config(page_title="ChatVPT", page_icon=":robot_face:", layout="wide")  

    # Set sidebar title
    st.sidebar.title("ChatVPT")
    
    # Initialize summary history in session state
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Display chat history using the first line of each summary
    st.sidebar.subheader("Chat History")
    if st.session_state["history"]:
        for summary in st.session_state["history"][-5:]:  # Show only the last 5 summaries
            first_line = summary.split("\n")[0]  # Extract the first line
            if len(first_line) > 50:  # Truncate if it's too long
                first_line = first_line[:50] + "..."

            # Expandable sections to show full summaries
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

                # Show a loading spinner while processing
                with st.spinner("🔍 Extracting subtitles and summarizing... This may take a moment!"):
                    # Fetch transcript from YouTube
                    list_text = yta.get_transcript(video_id, languages=[AVAILABLE_LANGUAGES[selected_lang]])
                    text = " ".join([d["text"] for d in list_text])

                    # Summarize using LLM
                    result = youtube_summarize(text)

                # Display the summary after processing
                st.success("✅ Summary is ready!")
                st.text_area("Summary:", result, height=300)

                # Save the summary to history
                st.session_state["history"].append(result)

            except Exception as e:
                st.error("⚠️ Cannot retrieve subtitles. Please check the language and try again." + e)
        else:
            st.error("⚠️ Please enter a YouTube URL.")

if __name__ == "__main__":
    main()
