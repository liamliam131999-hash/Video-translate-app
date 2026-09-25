    if input_type == "YouTube URL":
        yt_url = st.text_input("YouTube Video URL ထည့်ပါ (Shorts လင့်ခ်များပါ ထည့်နိုင်သည်):")
        if yt_url:
            try:
                video_id = ""
                # Extract Video ID for various YouTube URL formats (watch, youtu.be, shorts)
                if "v=" in yt_url:
                    video_id = yt_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in yt_url:
                    video_id = yt_url.split("youtu.be/")[1].split("?")[0]
                elif "/shorts/" in yt_url:
                    video_id = yt_url.split("/shorts/")[1].split("?")[0]
                
                if video_id:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'my'])
                    transcript_text = " ".join([t['text'] for t in transcript_list])
                    st.success("YouTube Transcript အောင်မြင်စွာ ရရှိပါပြီ!")
                    st.text_area("ရရှိလာသော Transcript:", transcript_text, height=150)
                else:
                    st.error("မှန်ကန်သော YouTube URL ထည့်ပါ။")
            except Exception as e:
                st.error(f"Transcript ထုတ်ယူရာတွင် အမှားရှိပါသည်: {e}")
