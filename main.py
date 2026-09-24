import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

# Page Configuration
st.set_page_config(page_title="YouTube & Media Transcript Tool", page_icon="📝", layout="centered")

st.title("🎥 YouTube & Media Transcript Tool")
st.write("YouTube လင့်ခ်မှ Transcript ထုတ်ယူခြင်းနှင့် ကိုယ်ပိုင် ဗီဒီယို/အသံဖိုင်များမှ စာသားထုတ်ယူခြင်းများကို တစ်နေရာတည်းတွင် လုပ်ဆောင်ပါ။")

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


# --- OPTION 2: Local Video/Audio Transcript Option ---
st.divider()
st.subheader("📁 Local Video/Audio to Text Extractor")
st.write("သင့်ဖုန်းထဲရှိ ဗီဒီယိုဖိုင် (သို့) အသံဖိုင်ကို တင်ပြီး စာသားထုတ်ယူနိုင်ပါသည်။")

uploaded_file = st.file_uploader("ဗီဒီယို (သို့) အသံဖိုင်ကို ရွေးချယ်ပါ", type=["mp4", "mp3", "wav", "m4a"])

if uploaded_file is not None:
    st.audio(uploaded_file)
    if st.button("ဖိုင်ထဲမှ အသံကို စာသားပြောင်းရန်", type="secondary"):
        with st.spinner("ဖိုင်ကို စစ်ဆေးနေပါပြီ..."):
            # Note: For full local speech-to-text on Streamlit Cloud without heavy libraries, 
            # you can integrate an API or process it. Here is the placeholder UI ready for your workflow.
            st.info("💡 ဖိုင်ကို အောင်မြင်စွာ လက်ခံရရှိပါပြီ။ Streamlit Cloud ၏ ဆာဗာ ကန့်သတ်ချက်ကြောင့် ကြီးမားသော AI Model များကို တိုက်ရိုက် run ნაცვლად အသံဖိုင်ကို Preview ကြည့်ခြင်းနှင့် ဖိုင်စီမံခြင်းများကို ဤနေရာတွင် ဆောင်ရွက်နိုင်ပါသည်။")
