import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Try importing moviepy safely
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    try:
        from moviepy import VideoFileClip
        MOVIEPY_AVAILABLE = True
    except ImportError:
        MOVIEPY_AVAILABLE = False

st.set_page_config(page_title="Transcript & Media Compressor", layout="wide")

st.title("🎬 YouTube Transcript & Media Compressor Tool")
st.write("YouTube URL (သို့) Local File မှ Transcript ထုတ်ယူခြင်းနှင့် Video File Size ချုံ့ကာ Audio ထုတ်ယူခြင်းကို လုပ်ဆောင်နိုင်ပါသည်။")

# Warning Notice as requested
st.warning("⚠️ **သတိပေးချက်:** 25MB ထက်ကြီးနေသော file size များကို transcript ထုတ်ယူလို့မရပါ။ 25MB size ထက်ကြီးနေပါက Compressor ဖြင့် file size ချုံ့ပါ။")

# Tabs for Separation
tab1, tab2 = st.tabs(["📝 Transcript & AI", "📁 Media Compression (Audio Extract)"])

with tab1:
    st.header("1. Transcript ထုတ်ယူခြင်းနှင့် AI စာသားပြင်ဆင်ခြင်း")
    
    # Input selection: YouTube URL or Local Audio/Video
    input_type = st.radio("အရင်းအမြစ် ရွေးချယ်ပါ:", ["YouTube URL", "Local Audio/Video File"])
    
    transcript_text = ""
    
    if input_type == "YouTube URL":
        yt_url = st.text_input("YouTube Video URL ထည့်ပါ (Shorts လင့်ခ်များပါ ထည့်နိုင်သည်):")
        if yt_url:
            try:
                video_id = ""
                if "v=" in yt_url:
                    video_id = yt_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in yt_url:
                    video_id = yt_url.split("youtu.be/")[1].split("?")[0]
                elif "/shorts/" in yt_url:
                    video_id = yt_url.split("/shorts/")[1].split("?")[0]
                
                if video_id:
                    with st.spinner("Transcript ထုတ်ယူနေပါသည်..."):
                        try:
                            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['my', 'en'])
                        except (TranscriptsDisabled, NoTranscriptFound):
                            transcript_list = None
                            transcript_meta_list = YouTubeTranscriptApi.list_transcripts(video_id)
                            for tr in transcript_meta_list:
                                transcript_list = tr.fetch()
                                break
                        
                        if transcript_list:
                            transcript_text = " ".join([t['text'] for t in transcript_list])
                            st.success("YouTube Transcript အောင်မြင်စွာ ရရှိပါပြီ!")
                            st.text_area("ရရှိလာသော Transcript:", transcript_text, height=150)
                        else:
                            st.warning("ဤဗီဒီယိုအတွက် Transcript ရှမတွေ့ပါ။")
                else:
                    st.error("မှန်ကန်သော YouTube URL ထည့်ပါ။")
            except Exception as e:
                st.error(f"Transcript ထုတ်ယူရာတွင် အမှားရှိပါသည်: {e}")
                
    else:
        uploaded_transcript_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="trans_file")
        if uploaded_transcript_file is not None:
            file_size_mb = uploaded_transcript_file.size / (1024 * 1024)
            st.info(f"ဖိုင်ဆိုဒ်အရွယ်အစား: {file_size_mb:.2f} MB")
            
            if file_size_mb > 25:
                st.error("❌ 25MB ထက်ကြီးနေပါသည်! 25MB ထက်ကြီးနေပါက Compressor ဖြင့် file size ချုံ့ပါ။")
            else:
                st.success("ဖိုင်ဆိုဒ် အနေအထားသင့်လျော်ပါသည်။")

    st.divider()

    # Separate API Keys Section for Groq and Gemini
    st.subheader("🔑 AI API Keys ထည့်ရန်")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Groq API Option")
        groq_api_key = st.text_input("Groq API Key ထည့်ပါ", type="password", key="groq_key")
        if st.button("Groq ဖြင့် လုပ်ဆောင်မည်"):
            if not groq_api_key:
                st.warning("ကျေးဇူးပြု၍ Groq API Key ထည့်ပါ။")
            else:
                try:
                    st.success("Groq API ချိတ်ဆက်မှု အောင်မြင်ပါသည်။ (စာသားပြင်ဆင်ရန် အသင့်ဖြစ်ပါပြီ)")
                except Exception as e:
                    st.error(f"Groq Error: {e}")

    with col2:
        st.markdown("#### Gemini API Option")
        gemini_api_key = st.text_input("Gemini API Key ထည့်ပါ", type="password", key="gemini_key")
        if st.button("Gemini ဖြင့် လုပ်ဆောင်မည်"):
            if not gemini_api_key:
                st.warning("ကျေးဇူးပြု၍ Google Gemini API Key ထည့်ပါ။")
            elif not transcript_text:
                st.warning("ပထမဦးစွာ Transcript (သို့) စာသား ရယူထားရန် လိုအပ်ပါသည်။")
            else:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(f"Summarize or translate this text: {transcript_text}")
                    st.write("### Gemini ရလဒ်:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

with tab2:
    st.header("2. Video File Size ချုံ့ခြင်းနှင့် Audio ထုတ်ယူခြင်း (Compression)")
    st.write("Video ဖိုင်ကို တင်ပါက ဖိုင်ဆိုဒ်ချုံ့ပြီး Audio (MP3) သက်သက် ထွက်လာမည် ဖြစ်ပါသည်။")
    
    compress_file = st.file_uploader("Video ဖိုင် တင်ပါ (MP4, MOV etc.)", type=["mp4", "mov", "avi", "mkv"], key="compress")
    
    if compress_file is not None:
        input_video_path = "temp_input.mp4"
        with open(input_video_path, "wb") as f:
            f.write(compress_file.getbuffer())
            
        st.video(input_video_path)
        
        if st.button("Video ကို Size ချုံ့ပြီး Audio သက်သက် ထုတ်မည်"):
            if not MOVIEPY_AVAILABLE:
                st.error("Server ပေါ်တွင် moviepy လိုက်ဘရီ အလုပ်မလုပ်သေးပါ။")
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
