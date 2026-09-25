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

    # Separate API Keys Section for Groq and Gemini with clear execution buttons
    st.subheader("🔑 AI API Keys နှင့် လုပ်ဆောင်ရန် ခလုတ်များ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Groq API Option")
        groq_api_key = st.text_input("Groq API Key ထည့်ပါ", type="password", key="groq_key")
        if st.button("Groq ဖြင့် စာသားပြင်ဆင်မည်"):
            if not groq_api_key:
                st.warning("ကျေးဇူးပြု၍ Groq API Key ထည့်ပါ။")
            elif not transcript_text:
                st.warning("ပထမဦးစွာ Transcript ရယူထားရန် လိုအပ်ပါသည်။")
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
            elif not transcript_text:
                st.warning("ပထမဦးစွာ Transcript ရယူထားရန် လိုအပ်ပါသည်။")
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
