import streamlit as st
from pydub import AudioSegment
from openai import OpenAI
import os

# OPEN_AI_API_KEY = st.secrets["opena_ai_api_key"]
OPEN_AI_API_KEY = "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"

class aduio_file_upload:

    def __init__(self) -> None:
        self.client = OpenAI(api_key=OPEN_AI_API_KEY)


    def audio_file(self):

    # Title of the app
        output_placeholder = st.empty()
        output_placeholder.empty()
        st.title("Audio Transcription")

        # File uploader for audio files
        audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "ogg"])
        
        # Check if an audio file has been uploaded
        if audio_file is not None:
            # Display the audio file details
            # st.write(f"**Filename:** {audio_file.name}")
            # st.write(f"**File type:** {audio_file.type}")
            # st.write(f"**File size:** {audio_file.size} bytes")
            
            # Play the uploaded audio file
            st.audio(audio_file, format=audio_file.type)
            file_name = audio_file.name
            print(file_name,type(file_name))
            # Save the uploaded audio file to the server (optional)
            with open("audio file/"+file_name, "wb") as f:
                f.write(audio_file.getbuffer())
            # st.success("Audio file saved successfully!")
            audio = AudioSegment.from_file("audio file/"+file_name)

            # Get the duration in milliseconds
            duration_ms = len(audio)

            # Convert milliseconds to seconds
            duration_min = duration_ms // (1000*60)

            print(f"Duration: {duration_min} minutes")
            print(file_name[:len(file_name)-4])
            if duration_min<=10 :
                audio_file=open("audio file/"+file_name,"rb")
                transcription = self.client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file
                        )
                # print(transcription.text)
                transcript_file_name = "Audio Transcription/"+file_name[:len(file_name)-4]+".txt"
                with open(transcript_file_name, "a") as file:
                    file.write(transcription.text)
                st.success("Audio Transcription Completed.")
                st.download_button(label= "Download Transcription File",
                                   data=transcription.text,
                                   file_name=transcript_file_name,
                                   mime="text/plain"
                                   )
            else:
                l=[]
                for i in range(0,duration_min,5):
                    l.append(i)
                l.append(duration_min)
                print(l)
                if ".mp3" in file_name:
                    audio =AudioSegment.from_mp3("audio file/"+file_name)
                elif ".wav" in file_name:
                    audio = AudioSegment.from_wav("audio file/"+file_name)
                elif ".ogg" in file_name:
                    audio = AudioSegment.from_ogg("audio file/"+file_name)
                
                for i in range(len(l)-1):
                    start = l[i]*60 * 1000
                    end = l[i+1]*60 * 1000

                    temp_aud_file = audio[start:end]
                    temp_aud_file.export("temp_audio/new.mp3",format ="mp3")
                    audio_file=open("temp_audio/new.mp3","rb")
                    transcription = self.client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file
                        )
                    # print(transcription.text)
                    transcript_file_name = "Audio Transcription/"+file_name[:len(file_name)-4]+".txt"
                    with open(transcript_file_name, "a") as file:
                        file.write(transcription.text+"/n")
                
                with open(transcript_file_name,'r') as file:
                    content=file.read()
                
                st.success("Audio Transcription Completed.")
                st.download_button(label= "Download Transcription File",
                                   data=content,
                                   file_name=transcript_file_name,
                                   mime="text/plain"
                                   )
            os.remove(transcript_file_name)



obj_audio_file_upload = aduio_file_upload()