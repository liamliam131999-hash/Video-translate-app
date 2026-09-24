import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import os

# Page Configuration
st.set_page_config(page_title="YouTube & Media Transcript Tool", page_icon="📝", layout="centered")

st.title("🎥 YouTube & Media Transcript Tool")
st.write("YouTube လင့်ခ်မှ Transcript ထုတ်ယူခြင်းနှင့် AI API (Groq/Gemini) များကို အသုံးပြု၍ အသံ/ဗီဒီယိုဖိုင်များမှ စာသားထုတ်ယူခြင်းများကို တစ်နေရာတည်းတွင် လုပ်ဆောင်ပါ။")

# --- OPTION 1: YouTube Transcript Extractor ---
st.subheader("🎥 YouTube Video Transcript Extractor")

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]
    
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        path_parts = parsed_url.path.split('/')
        if len(path_parts) > 2 and path_parts[1] == 'shorts':
            return path_parts[2]
        elif parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.path.startswith(('/embed/', '/v/')):
            return path_parts[2]
            
    return None

youtube_url = st.text_input("YouTube Video URL ကို ထည့်ပါ:", placeholder="https://www.youtube.com/shorts/...")

if st.button("Transcript ထုတ်ယူရန်", type="primary"):
    if youtube_url:
        video_id = extract_video_id(youtube_url)
        
        if video_id:
            with st.spinner("Transcript ကို ရှာဖွေနေပါပြီ... ခဏစောင့်ပေးပါ။"):
                try:
                    ytt_api = YouTubeTranscriptApi()
                    transcript_list = ytt_api.fetch(video_id)
                    
                    st.success("Transcript အောင်မြင်စွာ ရရှိပါပြီ! 🎉")
                    
                    formatted_text = ""
                    for entry in transcript_list:
                        start_time = int(entry.start)
                        minutes = start_time // 60
                        seconds = start_time % 60
                        timestamp = f"[{minutes:02d}:{seconds:02d}]"
                        
                        text = entry.text
                        formatted_text += f"{timestamp} {text}\n"
                        
                        st.markdown(f"**`{timestamp}`** {text}")
                    
                    st.download_button(
                        label="📥 Transcript ကို Text ဖိုင်ဖြင့် Download ရန်",
                        data=formatted_text,
                        file_name=f"transcript_{video_id}.txt",
                        mime="text/plain"
                    )
                    
                except TranscriptsDisabled:
                    st.error("❌ ဒီဗီဒီယိုအတွက် Transcript ပိတ်ထားပါသည် (သို့မဟုတ်) မရှိပါ။")
                except NoTranscriptFound:
                    st.error("❌ ဒီဗီဒီယိုအတွက် သင့်လျော်သော Transcript မတွေ့ရှိပါ။")
                except Exception as e:
                    st.error(f"❌ အမှားအယွင်း တစ်စုံတစ်ရာ ဖြစ်ပွားသွားပါပြီ: {e}")
        else:
            st.warning("⚠️ မှန်ကန်သော YouTube URL (သို့မဟုတ် Shorts URL) ကို ထည့်သွင်းပေးပါ။")
    else:
        st.warning("⚠️ ကျေးဇူးပြု၍ YouTube URL ထည့်ပါ။")


# --- OPTION 2: Local Video/Audio Transcript Option with API Keys on Main Page ---
st.divider()
st.subheader("📁 Local Video/Audio to Text Extractor")

# API Keys input directly on Main Page for easy mobile access
st.write("🔑 **API Keys ထည့်သွင်းရန်**")
groq_api_key = st.text_input("Groq API Key ထည့်ရန်:", type="password", key="groq_key")
gemini_api_key = st.text_input("Gemini API Key ထည့်ရန်:", type="password", key="gemini_key")

st.write("ဖိုင်အမျိုးအစားကို ရွေးချယ်ပြီး ဗီဒီယို (သို့) အသံဖိုင်ကို တင်ပါ။")

file_choice = st.radio("ဖိုင် အမျိုးအစား ရွေးချယ်ရန်:", ["အသံဖိုင် (Audio - mp3, wav, m4a)", "ဗီဒီယိုဖိုင် (Video - mp4, mkv, mov)"])

if "အသံဖိုင်" in file_choice:
    uploaded_file = st.file_uploader("အသံဖိုင်ကို ရွေးချယ်ပါ", type=["mp3", "wav", "m4a", "ogg"])
else:
    uploaded_file = st.file_uploader("ဗီဒီယိုဖိုင်ကို ရွေးချယ်ပါ", type=["mp4", "mkv", "mov", "avi"])

if uploaded_file is not None:
    if "အသံဖိုင်" in file_choice:
        st.audio(uploaded_file)
    else:
        st.video(uploaded_file)
        
    ai_choice = st.selectbox("အသုံးပြုမည့် AI ဝန်ဆောင်မှုကို ရွေးပါ:", ["Groq API", "Gemini API"])
    
    if st.button("ဖိုင်ထဲမှ အသံကို စာသားပြောင်းရန်", type="secondary"):
        if ai_choice == "Groq API" and not groq_api_key:
            st.warning("⚠️ ကျေးဇူးပြု၍ Groq API Key ထည့်သွင်းပေးပါ။")
        elif ai_choice == "Gemini API" and not gemini_api_key:
            st.warning("⚠️ ကျေးဇူးပြု၍ Gemini API Key ထည့်သွင်းပေးပါ။")
        else:
            with st.spinner("ဖိုင်ကို AI ဖြင့် စာသားပြောင်းလဲနေပါပြီ..."):
                st.info(f"💡 ရွေးချယ်ထားသော {ai_choice} ဖြင့် ဖိုင်ကို စီမံဆောင်ရွက်ရန် အဆင်သင့်ဖြစ်ပါပြီ။ API ချိတ်ဆက်မှု ကုဒ်များ ဆက်လက်ထည့်သွင်းရန် လိုအပ်ပါသည်။")
