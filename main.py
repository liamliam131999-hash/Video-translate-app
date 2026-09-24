import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs

# Page Configuration
st.set_page_config(page_title="YouTube Transcript Extractor", page_icon="📝", layout="centered")

st.title("🎥 YouTube Video Transcript Extractor")
st.write("YouTube Video သို့မဟုတ် Shorts Link ကို ထည့်သွင်းပြီး Transcript (စာသားများ) ကို အလွယ်တကူ ထုတ်ယူပါ။")

# Function to extract Video ID from various YouTube URL formats (including /shorts/)
def extract_video_id(url):
    parsed_url = urlparse(url)
    # Handle youtu.be links
    if parsed_url.hostname in ['youtu.be']:
        return parsed_url.path[1:]
    
    # Handle youtube.com links
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        path_parts = parsed_url.path.split('/')
        # Handle /shorts/VIDEO_ID
        if len(path_parts) > 2 and path_parts[1] == 'shorts':
            return path_parts[2]
        # Handle /watch?v=VIDEO_ID
        elif parsed_url.path == '/watch':
            return parse_qs(parsed_url.query).get('v', [None])[0]
        # Handle /embed/ or /v/
        elif parsed_url.path.startswith(('/embed/', '/v/')):
            return path_parts[2]
            
    return None

# Input field for YouTube URL
youtube_url = st.text_input("YouTube Video URL ကို ထည့်ပါ:", placeholder="https://www.youtube.com/shorts/...")

if st.button("Transcript ထုတ်ယူရန်", type="primary"):
    if youtube_url:
        video_id = extract_video_id(youtube_url)
        
        if video_id:
            with st.spinner("Transcript ကို ရှာဖွေနေပါပြီ... ခဏစောင့်ပေးပါ။"):
                try:
                    # Fetch transcript
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                    
                    st.success("Transcript အောင်မြင်စွာ ရရှိပါပြီ! 🎉")
                    
                    # Format transcript with timestamps
                    formatted_text = ""
                    for entry in transcript_list:
                        start_time = int(entry['start'])
                        minutes = start_time // 60
                        seconds = start_time % 60
                        timestamp = f"[{minutes:02d}:{seconds:02d}]"
                        
                        text = entry['text']
                        formatted_text += f"{timestamp} {text}\n"
                        
                        # Display on UI
                        st.markdown(f"**`{timestamp}`** {text}")
                    
                    # Download button for transcript
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
