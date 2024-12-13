#https://youtu.be/ysENqhc2bEI?si=6_9EQH03buoBi7vM

import tkinter as tk
from tkinter import messagebox
from pytube import YouTube

import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *

from pydub import AudioSegment

import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

import spacy


# Function to download the YouTube video in MP4 format
def download_video():
    video_url = url_entry.get()
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(
            file_extension='mp4').get_highest_resolution()
        stream.download()
        messagebox.showinfo("Download Complete",
                            "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create a label
label = tk.Label(root, text="Enter YouTube URL:")
label.pack(pady=10)

# Create an entry field to enter the URL
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Create a download button
download_button = tk.Button(root, text="Download MP4", command=download_video)
download_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()


# Function to convert wav into text
# create a speech recognition object
r = sr.Recognizer()

# a function to recognize speech in the audio file
# so that we don't repeat ourselves in in other functions


def transcribe_audio(path):
    # use the audio file as the audio source
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_google(audio_listened)
        # Write transcribe in text file
        filename = "CSD2.txt"
        if os.path.exists(filename):
            f = None
            try:
                f = open(filename, "a")
                data = text
                f.write(data + "\n")
            except Exception as e:
                print("Issues", e)
            finally:
                if f is not None:
                    f.close()
        else:
            print(filename, " does not exists")

###################################################################################
##############################################################################
    return text

# a function that splits the audio file into chunks on silence
# and applies speech recognition


def get_large_audio_transcription_on_silence(path):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=500,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS-14,
                              # keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text
    # return the text for all chunks detected
################################################################################################################################
    filename = "Transcript.txt"
    if os.path.exists(filename):
        f = None
        try:
            f = open(filename, "a")
            data = whole_text
            f.write(data + "\n")
        except Exception as e:
            print("issue", e)
        finally:
            if f is not None:
                f.close()
    else:
        print(filename, "does not exists")

################################################################################################################################
    return whole_text


# Funtion to convert mp3 to wav
def mp3_to_wav(mp3_file):
    sound = AudioSegment.from_mp3(mp3_file)
    wave_file = mp3_file[:-4] + ".wav"
    sound.export(wave_file, format="wav")
    print("Converted to wav")
    print("\nFull text:", get_large_audio_transcription_on_silence(wave_file))


# Funtion to convert mp4 to mp3
def convert_to_mp3():
    mp4_file = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if mp4_file:
        try:
            video = VideoFileClip(mp4_file)
            mp3_file = mp4_file[:-4] + ".mp3"
            video.audio.write_audiofile(mp3_file)
            video.close()
            messagebox.showinfo(
                "Conversion Complete", f"{mp4_file} converted to {mp3_file} successfully!")
            mp3_to_wav(mp3_file)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Create the main window
root = tk.Tk()
root.title("MP4 to MP3 Converter")

# Create a label
label = tk.Label(root, text="Select an MP4 file:")
label.pack(pady=10)

# Create a convert button
convert_button = tk.Button(root, text="Convert to MP3", command=convert_to_mp3)
convert_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()





# Function to extract keywords from a text file
nlp = spacy.load("en_core_web_sm")

def extract_keywords_from_file(file_path):
    keywords = []

    # Open the file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Process the text with spaCy
    doc = nlp(text)

    # Extract keywords (nouns and proper nouns)
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN']:
            keywords.append(token.text)

    return keywords

# Function to store keywords in a text file
def save_keywords_to_file(keywords, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for keyword in keywords:
            file.write(keyword + '\n')


# Example usage:
input_file_path = 'Transcript.txt'  # Replace with your input file path
output_file_path = 'keywords.txt'  # Replace with the desired output file name

keywords = extract_keywords_from_file(input_file_path)
save_keywords_to_file(keywords, output_file_path)

print(f"Keywords have been saved to '{output_file_path}'.")





# Function to extract unique words
def get_unique_words(file1, file2):
    # Read the contents of both files and split them into words
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        words1 = set(f1.read().split())
        words2 = set(f2.read().split())

    # Find the unique words in each file
    unique_words_in_file1 = words1 - words2
    unique_words_in_file2 = words2 - words1

    return unique_words_in_file1, unique_words_in_file2


if __name__ == "__main__":
    file1 = "keywords.txt"  # Replace with the path to your first text file
    file2 = "Dictionary.txt"  # Replace with the path to your second text file

    unique_words_in_file1, unique_words_in_file2 = get_unique_words(
        file1, file2)

    print("Unique words in Transcript.txt:", unique_words_in_file1)