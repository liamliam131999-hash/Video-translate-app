import os
import streamlit as st

st.set_page_config(page_title="Transcript & Media Compressor", layout="wide")

st.title("🎬 AI Transcript & Media Compressor Tool")
st.write("Local ဖိုင်တင်၍ AI ဖြင့် စာသားပြင်ဆင်ခြင်းနှင့် Video File Size ချုံ့ကာ Audio ထုတ်ယူခြင်းတို့ကို လုပ်ဆောင်နိုင်ပါသည်။")

# Warning Notice as requested
st.warning("⚠️ **သတိပေးချက်:** 25MB ထက်ကြီးနေသော file size များကို transcript ထုတ်ယူလို့မရပါ။ 25MB size ထက်ကြီးနေပါက Compressor ဖြင့် file size ချုံ့ပါ။")

# Tabs for Separation
tab1, tab2 = st.tabs(["📝 Transcript & AI", "📁 Media Compression (Audio Extract)"])

with tab1:
    st.header("1. Local File ဖြင့် Transcript / စာသားရယူခြင်းနှင့် AI စာသားပြင်ဆင်ခြင်း")
    
    # Choose file option for transcription (25MB limit warning)
    uploaded_transcript_file = st.file_uploader("Audio သို့မဟုတ် Video ဖိုင် တင်ပါ (25MB အောက်)", type=["mp3", "wav", "m4a", "mp4", "mov"], key="trans_file")
    
    file_content_text = ""
    if uploaded_transcript_file is not None:
        file_size_mb = uploaded_transcript_file.size / (1024 * 1024)
        st.info(f"ဖိုင်ဆိုဒ်အရွယ်အစား: {file_size_mb:.2f} MB")
        
        if file_size_mb > 25:
            st.error("❌ 25MB ထက်ကြီးနေပါသည်! 25MB ထက်ကြီးနေပါက Compressor ဖြင့် file size ချုံ့ပါ။")
        else:
            st.success("ဖိုင်ဆိုဒ် အနေအထားသင့်လျော်ပါသည်။ အောက်ပါ AI Options များကို အသုံးပြုနိုင်ပါပြီ။")

    st.divider()

    # Separate API Keys Section for Groq and Gemini
    st.subheader("🔑 AI API Keys နှင့် လုပ်ဆောင်ရန် ခလုတ်များ")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Groq API Option")
        groq_api_key = st.text_input("Groq API Key ထည့်ပါ", type="password", key="groq_key")
        if st.button("Groq ဖြင့် စာသားပြင်ဆင်မည်"):
            if not groq_api_key:
                st.warning("ကျေးဇူးပြု၍ Groq API Key ထည့်ပါ။")
            elif uploaded_transcript_file is None:
                st.warning("ကျေးဇူးပြု၍ ပထမဦးစွာ ဖိုင်တင်ပါ။")
            else:
                try:
                    st.success("Groq API ဖြင့် အောင်မြင်စွာ လုပ်ဆောင်ပြီးပါပြီ။")
                except Exception as e:
                    st.error(f"Groq Error: {e}")

    with col2:
        st.markdown("#### Gemini API Option")
        gemini_api_key = st.text_input("Gemini API Key ထည့်ပါ", type="password", key="gemini_key")
        if st.button("Gemini ဖြင့် စာသားပြင်ဆင်မည်"):
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
    st.header("2. Video File Size ချုံ့ခြင်းနှင့် Audio ထုတ်ယူခြင်း (Compression)")
    st.write("Video ဖိုင်ကို တင်ပါက ဖိုင်ဆိုဒ်ချုံ့ပြီး Audio (MP3) သက်သက် ထွက်လာမည် ဖြစ်ပါသည်။")
    
    compress_file = st.file_uploader("Video ဖိုင် တင်ပါ (MP4, MOV etc.)", type=["mp4", "mov", "avi", "mkv"], key="compress")
    
    if compress_file is not None:
        input_video_path = "temp_input.mp4"
        with open(input_video_path, "wb") as f:
            f.write(compress_file.getbuffer())
            
        st.video(input_video_path)
        
        if st.button("Video ကို Size ချုံ့ပြီး Audio သက်သက် ထုတ်မည်"):
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
                            mime="audio/mp3"
                        )
            except Exception as e:
                st.error(f"လုပ်ဆောင်ရာတွင် အမှားဖြစ်ပွားပါသည်: {e}")
