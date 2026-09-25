import os
import streamlit as st

st.set_page_config(page_title="My Transcriber", layout="wide")

# Custom CSS for Dark Modern App UI and Side-by-Side Cards
st.markdown("""
<style>
    .stApp {
        background-color: #070913;
        color: #f8fafc;
    }
    
    /* Header Banner Card */
    .header-card {
        background: linear-gradient(135deg, #0f172a 100%, #1e293b 0%);
        border: 1px solid #1e293b;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Notice Warning Box */
    .notice-box {
        background-color: rgba(234, 179, 8, 0.08);
        border: 1px solid rgba(234, 179, 8, 0.2);
        padding: 8px 12px;
        border-radius: 12px;
        color: #fbbf24;
        font-size: 0.85rem;
        margin-top: 10px;
    }

    /* Grid Feature Cards */
    .grid-card {
        background: linear-gradient(145deg, #0f172a 0%, #0b0f19 100%);
        border: 1px solid #1e293b;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 10px;
        min-height: 140px;
        text-align: center;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# App Header Section
st.markdown("""
<div class="header-card">
    <div style="font-size: 2.2rem;">⚡</div>
    <h2 style="color: #38bdf8; margin: 5px 0 2px 0;">My Transcriber</h2>
    <p style="color: #64748b; font-size: 0.8rem; letter-spacing: 1px;">Audio • Video • Transcript • Compressor</p>
    <div class="notice-box">
        ⚠️ တိုက်ရိုက်တင်မည့်ဖိုင်သည် 25MB အောက် ဖြစ်ရပါမည်။
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize Session State for Navigation
if 'nav_page' not in st.session_state:
    st.session_state['nav_page'] = "Home"

# Navigation Menu Bar (Home, Groq, Gemini, Compressor)
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state['nav_page'] = "Home"
with nav_col2:
    if st.button("🎙️ Groq", use_container_width=True):
        st.session_state['nav_page'] = "Groq"
with nav_col3:
    if st.button("✨ Gemini", use_container_width=True):
        st.session_state['nav_page'] = "Gemini"
with nav_col4:
    if st.button("📊 Comp", use_container_width=True):
        st.session_state['nav_page'] = "Compressor"

st.divider()

# Render content based on selected navigation page
page = st.session_state['nav_page']

if page == "Home":
    # Side-by-side layout (2 columns per row) for clean compact look
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("""
        <div class="grid-card">
            <div class="card-icon">🎙️</div>
            <h4 style="color: #38bdf8; margin: 0 0 5px 0; font-size: 1rem;">Groq Whisper</h4>
            <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">Fast transcription</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ဝင်ရန် (Groq)", key="btn_groq_go", use_container_width=True):
            st.session_state['nav_page'] = "Groq"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="grid-card">
            <div class="card-icon">📈</div>
            <h4 style="color: #38bdf8; margin: 0 0 5px 0; font-size: 1rem;">Compressor</h4>
            <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">25MB local sizing</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ဝင်ရန် (Compressor)", key="btn_comp_go", use_container_width=True):
            st.session_state['nav_page'] = "Compressor"
            st.rerun()

    with col_b:
        st.markdown("""
        <div class="grid-card">
            <div class="card-icon">✨</div>
            <h4 style="color: #c084fc; margin: 0 0 5px 0; font-size: 1rem;">Gemini AI</h4>
            <p style="color: #94a3b8; font-size: 0.75rem; margin: 0;">Audio/Video text</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ဝင်ရန် (Gemini)", key="btn_gem_go", use_container_width=True):
            st.session_state['nav_page'] = "Gemini"
            st.rerun()

elif page == "Groq":
    st.markdown("### 🎙️ Groq Whisper Transcription")
    groq_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="groq_up")
    groq_key = st.text_input("Groq API Key ထည့်ပါ", type="password", key="groq_k")
    
    if st.button("Groq ဖြင့် စာသားထုတ်မည်", use_container_width=True):
        if not groq_key or not groq_file:
            st.warning("API Key နှင့် ဖိုင်ကို အပြည့်အစုံ ထည့်ပါ။")
        else:
            st.success("Groq ဖြင့် လုပ်ဆောင်နေပါပြီ...")
            
    st.markdown("#### 📋 ထွက်လာသော Transcript စာသား")
    st.text_area("Transcript Output", "ဒီနေရာတွင် Transcript စာသားများ ပေါ်လာမည် ဖြစ်ပါသည်။", height=150, key="groq_out")
    st.info("💡 အထက်ပါ စာသားကို Copy ကူးယူနိုင်ပါသည်။")

elif page == "Gemini":
    st.markdown("### ✨ Gemini Audio/Video Transcription")
    gem_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="gem_up")
    gem_key = st.text_input("Gemini API Key ထည့်ပါ", type="password", key="gem_k")
    
    if st.button("Gemini ဖြင့် လုပ်ဆောင်မည်", use_container_width=True):
        if not gem_key or not gem_file:
            st.warning("API Key နှင့် ဖိုင်ကို အပြည့်အစုံ ထည့်ပါ။")
        else:
            st.success("Gemini ဖြင့် လုပ်ဆောင်ပြီးပါပြီ။")

elif page == "Compressor":
    st.markdown("### 📊 Smart Compressor & Audio Extractor")
    comp_file = st.file_uploader("Video ဖိုင် တင်ပါ (MP4, MOV etc.)", type=["mp4", "mov", "avi", "mkv"], key="comp_up")
    
    if comp_file is not None:
        input_path = "temp_input.mp4"
        with open(input_path, "wb") as f:
            f.write(comp_file.getbuffer())
        st.video(input_path)
        
        if st.button("Video ဖိုင်ဆိုဒ်ချုံ့ပြီး Audio ထုတ်မည်", use_container_width=True):
            try:
                from moviepy.editor import VideoFileClip
                with st.spinner("ဖိုင်ကို လုပ်ဆောင်နေပါပြီ..."):
                    out_audio = "output_audio.mp3"
                    clip = VideoFileClip(input_path)
                    clip.audio.write_audiofile(out_audio)
                    clip.close()
                    st.success("အောင်မြင်စွာ ချုံ့ပြီးပါပြီ!")
                    with open(out_audio, "rb") as af:
                        st.download_button("📥 Audio ဖိုင်ကို Download ရယူရန်", af, file_name="compressed.mp3", mime="audio/mp3", use_container_width=True)
            except Exception as e:
                st.error(f"အမှားဖြစ်ပွားပါသည်: {e}")
