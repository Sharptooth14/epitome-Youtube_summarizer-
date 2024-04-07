from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
# load all the environment variables


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """ You are a Youtube video summarizer. You will be summarizing the entire video and providing the important summary in points within 500 words. Please provide the summary of text given here : """


# getting the transcript from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " "
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript

    except Exception as e:
        raise e

# getting the summary based on prompt google_gemini


def generate_gemini_content(transcript_text, prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("Youtube Transcript Summarizer")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(
        f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Deatailed Summary:")
        st.write(summary)
