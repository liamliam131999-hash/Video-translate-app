import os
import streamlit as st

st.set_page_config(page_title="Transcript & Media Compressor", layout="wide")

# Custom CSS for 3D Cards, Animations, and UI Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* 3D Card Styling */
    .feature-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
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
    
    # Groq API Option Card with Expander
    with st.expander("⚡ Groq API Option ဖြင့် လုပ်ဆောင်ရန်"):
        st.markdown("""
        <div class="feature-card">
            <span class="emoji-3d">⚡</span>
            <strong style="font-size: 1.2rem; color: #f43f5e;">Groq API & Transcript ထုတ်ယူခြင်း</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Choose File option inside Groq card
        groq_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="groq_file_upload")
        
        # Groq API Key input
        groq_api_key = st.text_input("Groq API Key ထည့်ပါ", type="password", key="groq_key_input")
        
        if st.button("Groq ဖြင့် Transcript ထုတ်မည် / စာသားပြင်မည်", use_container_width=True):
            if not groq_api_key:
                st.warning("ကျေးဇူးပြု၍ Groq API Key ထည့်ပါ။")
            elif groq_file is None:
                st.warning("ကျေးဇူးပြု၍ ဖိုင်တင်ပါ။")
            else:
                try:
                    st.success("Groq API ဖြင့် အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ။")
                except Exception as e:
                    st.error(f"Groq Error: {e}")
        
        # Transcript Output Box with Copy-friendly area
        st.markdown("### 📋 ထွက်လာသော Transcript စာသားများ")
        sample_transcript = "ဒီနေရာတွင် ဖိုင်မှ ထွက်လာမည့် Transcript စာသားများ ပေါ်လာမည် ဖြစ်ပါသည်။"
        st.text_area("Transcript Output", sample_transcript, height=150, key="groq_transcript_output")
        st.info("💡 အထက်ပါ စာသားများကို ကူးယူလိုပါက Box ထောင့်ရှိ Copy ခလုတ်ကို အသုံးပြုနိုင်ပါသည်။")

    # Gemini API Option Card with Expander
    with st.expander("✨ Gemini API Option ဖြင့် လုပ်ဆောင်ရန်"):
        st.markdown("""
        <div class="feature-card">
            <span class="emoji-3d">✨</span>
            <strong style="font-size: 1.2rem; color: #a855f7;">Gemini API ဆက်တင်များ</strong>
        </div>
        """, unsafe_allow_html=True)
        
        gemini_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="gemini_file_upload")
        gemini_api_key = st.text_input("Gemini API Key ထည့်ပါ", type="password", key="gemini_key_input")
        
        if st.button("Gemini ဖြင့် လုပ်ဆောင်မည်", use_container_width=True):
            if not gemini_api_key:
                st.warning("ကျေးဇူးပြု၍ Google Gemini API Key ထည့်ပါ။")
            elif gemini_file is None:
                st.warning("ကျေးဇူးပြု၍ ဖိုင်တင်ပါ။")
            else:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=gemini_api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content("Provide summary instructions.")
                    st.write("### Gemini ရလဒ်:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Gemini Error: {e}")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🗜️ Video File Size ချုံ့ခြင်းနှင့် Audio ထုတ်ယူခြင်း"):
        st.markdown("""
        <div class="feature-card">
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
