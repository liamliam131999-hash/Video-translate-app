import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import yt_dlp
import os

# Page Configuration
st.set_page_config(page_title="YouTube & Douyin Tool", page_icon="🎬", layout="centered")

st.title("🎬 YouTube & Douyin Media Tool")
st.write("YouTube Video Transcript ထုတ်ယူခြင်းနှင့် Douyin ဗီဒီယို ဒေါင်းလုပ်ဆွဲခြင်းများကို တစ်နေရာတည်းတွင် လုပ်ဆောင်ပါ။")

# --- PART 1: YouTube Transcript Extractor ---
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


# --- PART 2: Douyin Video Downloader ---
st.divider()
st.subheader("📥 Douyin Video Downloader (Watermark Free)")

douyin_url = st.text_input("Douyin Video Link ကို ထည့်ပါ:", placeholder="https://v.douyin.com/...")

if st.button("Douyin ဗီဒီယို Download ရန်", type="secondary"):
    if douyin_url:
        with st.spinner("Douyin ဗီဒီယိုကို ရယူနေပါပြီ... ခဏစောင့်ပေးပါ။"):
            try:
                ydl_opts = {
                    'outtmpl': 'douyin_video.mp4',
                    'format': 'best',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(douyin_url, download=True)
                    filename = ydl.prepare_filename(info)
                
                st.success("ဗီဒီယိုကို အောင်မြင်စွာ ရယူပြီးပါပြီ! 🎉")
                
                st.video(filename)
                
                with open(filename, "rb") as file:
                    st.download_button(
                        label="📥 ဗီဒီယိုဖိုင်ကို Download ဆွဲရန်",
                        data=file,
                        file_name="douyin_download.mp4",
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"❌ ဗီဒီယိုဒေါင်းလုပ်ဆွဲရာတွင် အမှားအယွင်းရှိပါသည်: {e}")
    else:
        st.warning("⚠️ ကျေးဇူးပြု၍ Douyin URL ထည့်ပါ။")
