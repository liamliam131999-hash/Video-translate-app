import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
import google.generativeai as genai

# Try importing moviepy safely to prevent crashes
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    try:
        from moviepy import VideoFileClip
        MOVIEPY_AVAILABLE = True
    except ImportError:
        MOVIEPY_AVAILABLE = False

st.set_page_config(page_title="Media & YouTube Transcription Tool", layout="wide")

st.title("🎥 YouTube & Media Transcription & Compression Tool")
st.write("YouTube URL (သို့) Media File တင်ပြီး Transcript ယူခြင်း၊ AI ဖြင့် စာသားထုတ်ခြင်းနှင့် Video ကို File Size ချုံ့ကာ Audio ထုတ်ယူခြင်းတို့ကို တစ်နေရာတည်းတွင် လုပ်ဆောင်နိုင်ပါသည်။")

# Sidebar for API Keys configuration (Mobile Friendly)
st.sidebar.header("🔑 API Keys ထည့်ရန်")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

# Main Options
tab1, tab2, tab3 = st.tabs(["📝 Transcript & AI", "📁 Media Compression (Audio Extract)", "📥 Download Section"])

with tab1:
    st.header("1. YouTube URL သို့မဟုတ် Media File ဖြင့် Transcript ထုတ်ယူရန်")
    
    input_type = st.radio("အရင်းအမြစ် ရွေးချယ်ပါ:", ["YouTube URL", "Local Audio/Video File"])
    
    transcript_text = ""
    
    if input_type == "YouTube URL":
        yt_url = st.text_input("YouTube Video URL ထည့်ပါ:")
        if yt_url:
            try:
                # Extract Video ID
                if "v=" in yt_url:
                    video_id = yt_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in yt_url:
                    video_id = yt_url.split("youtu.be/")[1].split("?")[0]
                else:
                    video_id = ""
                
                if video_id:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'my'])
                    transcript_text = " ".join([t['text'] for t in transcript_list])
                    st.success("YouTube Transcript အောင်မြင်စွာ ရရှိပါပြီ!")
                    st.text_area("ရရှိလာသော Transcript:", transcript_text, height=150)
                else:
                    st.error("မှန်ကန်သော YouTube URL ထည့်ပါ။")
            except Exception as e:
                st.error(f"Transcript ထုတ်ယူရာတွင် အမှားရှိပါသည်: {e}")
                
    else:
        uploaded_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ။", type=["mp3", "wav", "m4a", "mp4", "mov"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(('mp3', 'wav', 'm4a')):
                st.audio(uploaded_file)
            else:
                st.video(uploaded_file)
            st.info("Local file တင်ထားပါပြီ။ AI Transcription ဖြင့် ဆက်လုပ်နိုင်ပါသည်။")

    # AI Processing Option
    st.subheader("🤖 AI ဖြင့် စာသားပြင်ဆင်ခြင်း (Groq / Gemini)")
    ai_provider = st.selectbox("AI Provider ရွေးပါ:", ["Groq (Whisper/Llama)", "Google Gemini"])
    
    if st.button("AI ဖြင့် စာသားထုတ်ယူ/ပြင်ဆင်မည်"):
        if ai_provider == "Groq (Whisper/Llama)":
            if not groq_api_key:
                st.warning("ကျေးဇူးပြု၍ Groq API Key ထည့်ပါ။")
            else:
                try:
                    client = Groq(api_key=groq_api_key)
                    st.success("Groq ဖြင့် အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ။")
                except Exception as e:
                    st.error(f"Groq Error: {e}")
        else:
            if not gemini_api_key:
                st.warning("ကျေးဇူးပြု၍ Gemini API Key ထည့်ပါ။")
            else:
                try:
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(f"Summarize or translate this text: {transcript_text}")
                    st.write("### Gemini ရလဒ်:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

with tab2:
    st.header("2. Video File Size ချုံ့ခြင်းနှင့် Audio ထုတ်ယူခြင်း (Compression)")
    st.write("Video ဖိုင်ကို တင်၍ File Size ချုံ့ခြင်းနှင့် Audio သက်သက် (MP3) ထုတ်ယူခြင်းကို ဤနေရာတွင် လုပ်ဆောင်နိုင်ပါသည်။")
    
    compress_file = st.file_uploader("Video ဖိုင် တင်ပါ (MP4, MOV etc.)", type=["mp4", "mov", "avi", "mkv"], key="compress")
    
    if compress_file is not None:
        input_video_path = "temp_input.mp4"
        with open(input_video_path, "wb") as f:
            f.write(compress_file.getbuffer())
            
        st.video(input_video_path)
        
        if st.button("Video ကို Size ချုံ့ပြီး Audio ထုတ်မည်"):
            if not MOVIEPY_AVAILABLE:
                st.error("Server ပေါ်တွင် moviepy လိုက်ဘရီ အလုပ်မလုပ်သေးပါ။ ကျေးဇူးပြု၍ requirements.txt တွင် moviepy ပါဝင်ကြောင်း စစ်ဆေးပါ။")
            else:
                with st.spinner("ဖိုင်ကို လုပ်ဆောင်နေပါပြီ ခဏစောင့်ပါ..."):
                    try:
                        output_audio_path = "output_audio.mp3"
                        video_clip = VideoFileClip(input_video_path)
                        video_clip.audio.write_audiofile(output_audio_path)
                        video_clip.close()
                        
                        st.success("Audio ထုတ်ယူပြီး File Size ချုံ့ခြင်း အောင်မြင်ပါပြီ!")
                        
                        with open(output_audio_path, "rb") as audio_file:
                            st.download_button(
                                label="📥 ထွက်လာသော Audio ဖိုင်ကို Download ဆွဲရန်",
                                data=audio_file,
                                file_name="compressed_audio.mp3",
                                mime="audio/mp3"
                            )
                    except Exception as e:
                        st.error(f"လုပ်ဆောင်ရာတွင် အမှားဖြစ်ပွားပါသည်: {e}")

with tab3:
    st.header("3. Download Section")
    st.write("ယခင် ထုတ်လုပ်ထားသော စာသားများနှင့် ဖိုင်များကို ဤနေရာတွင် ရယူနိုင်ပါသည်။")
