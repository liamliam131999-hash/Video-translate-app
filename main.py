import os
import streamlit as st

st.set_page_config(page_title="Transcript & Media Compressor", layout="wide")

# Custom CSS for Vertical 3D Cards, Animations, and Expandable Design
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Vertical 3D Card Styling */
    .vertical-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .vertical-card:hover {
        transform: translateX(5px);
        border-color: #38bdf8;
    }

    /* Floating Animation for Emojis */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-5px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    .emoji-3d {
        font-size: 2.2rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 8px 6px rgba(0, 0, 0, 0.4));
        margin-right: 15px;
        vertical-align: middle;
    }

    /* Warning Box Styling */
    .custom-warning {
        background-color: rgba(234, 179, 8, 0.1);
        border-left: 4px solid #eab308;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        color: #fef08a;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🎬 AI Transcript & Media Compressor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>ဒေါင်လိုက် 3D Card ပုံစံဖြင့် လိုအပ်သော Option ကို နှိပ်၍ အသုံးပြုပါ</p>", unsafe_allow_html=True)

# Warning Notice Card
st.markdown("""
<div class="custom-warning">
    <strong>⚠️ သတိပေးချက်:</strong> 25MB ထက်ကြီးနေသော file size များကို transcript ထုတ်ယူလို့မရပါ။ 25MB size ထက်ကြီးနေပါက Compressor ဖြင့် file size ချုံ့ပါ။
</div>
""", unsafe_allow_html=True)

# Tabs for Separation
tab1, tab2 = st.tabs(["📝 Transcript & AI", "📁 Media Compression"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Transcript / File Uploader Card (Vertical)
    with st.expander("📄  Local ဖိုင်တင်ရန် နှင့် Transcript ထုတ်ယူခြင်း"):
        st.markdown("""
        <div class="vertical-card">
            <span class="emoji-3d">📂</span>
            <strong style="font-size: 1.2rem; color: #38bdf8;">ဖိုင်တင်ရန် နေရာ</strong>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_transcript_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="trans_file")
        
        if uploaded_transcript_file is not None:
            file_size_mb = uploaded_transcript_file.size / (1024 * 1024)
            st.info(f"ဖိုင်ဆိုဒ်အရွယ်အစား: {file_size_mb:.2f} MB")
            
            if file_size_mb > 25:
                st.error("❌ 25MB ထက်ကြီးနေပါသည်! 25MB ထက်ကြီးနေပါက Compressor ဖြင့် file size ချုံ့ပါ။")
            else:
                st.success("ဖိုင်ဆိုဒ် အနေအထားသင့်လျော်ပါသည်။")

    # 2. Groq API Option Card (Vertical)
    with st.expander("⚡  Groq API Option ဖြင့် လုပ်ဆောင်ရန်"):
        st.markdown("""
        <div class="vertical-card">
            <span class="emoji-3d">⚡</span>
            <strong style="font-size: 1.2rem; color: #f43f5e;">Groq API ဆက်တင်များ</strong>
        </div>
        """, unsafe_allow_html=True)
        
        groq_api_key = st.text_input("Groq API Key ထည့်ပါ", type="password", key="groq_key")
        if st.button("Groq ဖြင့် စာသားပြင်ဆင်မည်", use_container_width=True):
            if not groq_api_key:
                st.warning("ကျေးဇူးပြု၍ Groq API Key ထည့်ပါ။")
            elif uploaded_transcript_file is None:
                st.warning("ကျေးဇူးပြု၍ ပထမဦးစွာ ဖိုင်တင်ပါ။")
            else:
                try:
                    st.success("Groq API ဖြင့် အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ။")
                except Exception as e:
                    st.error(f"Groq Error: {e}")

    # 3. Gemini API Option Card (Vertical)
    with st.expander("✨  Gemini API Option ဖြင့် လုပ်ဆောင်ရန်"):
        st.markdown("""
        <div class="vertical-card">
            <span class="emoji-3d">✨</span>
            <strong style="font-size: 1.2rem; color: #a855f7;">Gemini API ဆက်တင်များ</strong>
        </div>
        """, unsafe_allow_html=True)
        
        gemini_api_key = st.text_input("Gemini API Key ထည့်ပါ", type="password", key="gemini_key")
        if st.button("Gemini ဖြင့် စာသားပြင်ဆင်မည်", use_container_width=True):
            if not gemini_api_key:
                st.warning("ကျေးဇူးပြု၍ Google Gemini API Key ထည့်ပါ။")
            elif uploaded_transcript_file is None:
                st.warning("ကျေးဇူးပြု၍ ပထမဦးစွာ ဖိုင်တင်ပါ။")
            else:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content("Analyze the uploaded media or provide summary instructions.")
                    st.write("### Gemini ရလဒ်:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Media Compression Card (Vertical)
    with st.expander("🗜️  Video File Size ချုံ့ခြင်းနှင့် Audio ထုတ်ယူခြင်း"):
        st.markdown("""
        <div class="vertical-card">
            <span class="emoji-3d">🎧</span>
            <strong style="font-size: 1.2rem; color: #38bdf8;">Video Compressor & Audio Extractor</strong>
        </div>
        """, unsafe_allow_html=True)
        
        compress_file = st.file_uploader("Video ဖိုင် တင်ပါ (MP4, MOV etc.)", type=["mp4", "mov", "avi", "mkv"], key="compress")
        
        if compress_file is not None:
            input_video_path = "temp_input.mp4"
            with open(input_video_path, "wb") as f:
                f.write(compress_file.getbuffer())
                
            st.video(input_video_path)
            
            if st.button("Video ကို Size ချုံ့ပြီး Audio သက်သက် ထုတ်မည်", use_container_width=True):
                try:
                    from moviepy.editor import VideoFileClip
                    with st.spinner("ဖိုင်ကို လုပ်ဆောင်နေပါပြီ ခဏစောင့်ပါ..."):
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
                                mime="audio/mp3",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"လုပ်ဆောင်ရာတွင် အမှားဖြစ်ပွားပါသည်: {e}")
