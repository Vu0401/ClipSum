# ClipSum – Smart YouTube Video Summarizer 🚀


**YouTube-Summarize** is a Streamlit-based web application that extracts and summarizes transcripts from YouTube videos using AI-powered language models. It helps users quickly understand video content by providing structured, easy-to-read summaries.  

🔗 **Live Demo:** [ClipSum](https://clipsum.streamlit.app)  

## ✨ Features  
- 🔍 **Automatic Transcript Retrieval** – Fetches subtitles from YouTube videos in the selected language.  
- 📝 **AI-Powered Summarization** – Uses an LLM (Large Language Model) to generate structured, bullet-point summaries.  
- 📌 **History Tracking** – Stores recent summaries for quick access and review.  
- 🎨 **User-Friendly UI** – Built with Streamlit for a clean and interactive experience.  

## 🚀 How It Works  
1. Enter a **YouTube video URL**.  
2. Select the **subtitle language**.  
3. Click **Summarize 🚀** to generate a structured summary.  
4. View and scroll through the summary in a bordered, scrollable container.  

## 🔧 Technologies Used  
- **Python** (Core application)  
- **Streamlit** (Web UI)  
- **YouTube Transcript API** (Subtitle extraction)  
- **LLM-based Summarization** (AI-generated summaries)  

## 🛠️ Local Installation  

```bash
# Clone the repository
git clone https://github.com/Vu0401/ClipSum.git

# Navigate to the project directory
cd ClipSum

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

> ⚠️ **Important:** Before running the app, create a `.env` file in the project directory and add your **GEMINI_API_KEY**:  
> ```  
> GEMINI_API_KEY="your_api_key_here"  
> ```  
> This is required for AI-powered search to function properly.
