import os
import requests
import re
from pytube import YouTube
from moviepy.editor import *

def get_links(query):
    query = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    html = response.text
    links = re.findall('"/watch\?v=(.{11})"', html)
    return [f"https://www.youtube.com/watch?v={link}" for link in links]

def download_video(link, folder):
    yt = YouTube(link)
    stream = yt.streams.first()
    stream.download(folder)
    print("Video Downloaded")
    
def convert_to_audio(folder):
    files_in_folder = os.listdir(folder)
    print("Files in folder:", files_in_folder)
    for filename in files_in_folder:
        if filename.endswith(".mp4"):
            video_path = os.path.join(folder, filename)
            audio_path = os.path.join(folder, filename.split(".")[0] + ".mp3")
            try:
                video = VideoFileClip(video_path)
                audio = video.audio
                audio.write_audiofile(audio_path)
                print(f"Converted {filename} file to audio successfully")
                video.close()
            except Exception as e:
                print(f"Error converting {filename} to audio: {e}")


            
def cutting_audio(folder, seconds):
    for audio_file in os.listdir(folder):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(folder, audio_file)
            cut_audio_path = os.path.join(folder, audio_file)
            audio = AudioFileClip(audio_path)
            cutting_audio = audio.subclip(0,seconds)
            cutting_audio.write_audiofile(cut_audio_path)
            
def merge_audio(folder, output_filename):
    audio_clips = []
    for filename in os.listdir(folder):
        if filename.endswith(".mp3") or filename.endswith(".wav"):
            audio_clip = AudioFileClip(os.path.join(folder, filename))
            audio_clips.append(audio_clip)
    if not audio_clips:
        print("No audio files found in the folder.")
        return None

    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile(output_filename)
    print("Merge Successful")

    # Close all AudioFileClip instances
    for audio_clip in audio_clips:
        audio_clip.close()

    return output_filename



def folder1(folder,links):
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for link in links:
        download_video(link, folder)

def main():
    singer = input("Enter the name of the singer: ")
    seconds = int(input("Enter the duration of each audio clip (in seconds): "))
    num = int(input("Enter the number of videos to download: "))
    output_filename = input("Enter the name of the output audio file: ")

    print(f"Singer: {singer}")
    
    folder = "vid"
    links = get_links(singer)[:num]
    
    print("Links found:")
    print(links)
    
    if not links:
        print("No videos found for the given singer.")
        return
    
    folder1(folder, links)
    convert_to_audio(folder)
    cutting_audio(folder, seconds)
    merge_audio(folder, output_filename)


if _name_ == "_main_":
    main()
