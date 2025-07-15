import os
from datetime import datetime
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
from playsound import playsound
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
import io
import requests
import time
import json
# import vlc
import sys
import subprocess
import pyautogui

# Redirect all output to log file
logfile_path = "vlc_assistant.log"
sys.stdout = open(logfile_path, 'a', buffering=1, encoding='utf-8')
sys.stderr = sys.stdout

#Set language
language = 'en'

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
# Pause timer in middle of sentence
r.pause_threshold = 2.0
r.non_speaking_duration = 0.5
r.energy_threshold = 400
r.dynamic_energy_threshold = True

tts_engine = 'gtts'  # select from 'gtts', 'pyttsx3', 'openai'

engine = pyttsx3.init()
voice = engine.getProperty('voices')[0]
engine.setProperty('voice', voice.id)

#Greeting
greetings = [
             "Hello, how can I help you today?",
             "Hi, how can I help?",
             ]

messages = []

# # Create VLC instance
# instance = vlc.Instance()

# # Create a new MediaPlayer
# player = instance.media_player_new()

#VLC Set
vlc_process = None
#VLC local path
#Open directory file
filename = "vlc_path.txt"
try:
    with open(filename, 'r') as f:
        vlc_path = f.read().strip()

    print("Directory read from file:", vlc_path)
except Exception as e:
    print(f"Something went wrong: {e}")
    sys.exit(f"Error occured reading file {e}, existing.")

# vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller stores temp folder path here
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Listening Chime
listen_chime = resource_path("listen_chime.mp3")
end_chime = resource_path("end.mp3")

#Open directory file
filename = "video_directory.txt"
try:
    with open(filename, 'r') as f:
        directory_path = f.read().strip()

    print("Directory read from file:", directory_path)
except Exception as e:
    print(f"Something went wrong: {e}")
    sys.exit(f"Error occured reading file {e}, existing.")




# #player pause
# def pause_if_playing(player):
#     if player.is_playing():
#         player.pause()
#         print("Paused playback.")
#     else:
#         print("Playback was not active.")

# #player resume
# def play_if_paused(player):
#     state = player.get_state()
#     # vlc.State.Paused means paused
#     if state == vlc.State.Paused:
#         player.play()
#         print("Resumed playing.")
#     else:
#         print(f"Player state is {state}, not paused.")

# def close_vlc_player(player):
#     """
#     Stops playback and closes the VLC player if it's active.
    
#     Args:
#         player: vlc.MediaPlayer() object
#     """
#     if player is not None:
#         state = player.get_state()
#         if state in [vlc.State.Playing, vlc.State.Paused]:
#             player.stop()
#             print("VLC player stopped.")
#         else:
#             print(f"VLC player is in state: {state}. No action needed.")
#     else:
#         print("VLC player is not initialized.")

# import vlc

# def close_player_if_ended(player):
#     """
#     If the VLC player's current media has finished (State.Ended),
#     stop playback and release the player resources, and speak a message.
#     """
#     if player is None:
#         return

#     state = player.get_state()
#     if state == vlc.State.Ended:
#         print("VLC player closed (media ended).")

#         # Speak the message
#         message = "Closing player as video has ended."
#         if tts_engine == 'pyttsx3':
#             engine.say(message)
#             engine.runAndWait()
#         elif tts_engine == 'gtts':
#             tts = gTTS(text=message, lang=language)
#             mp3_fp = io.BytesIO()
#             tts.write_to_fp(mp3_fp)
#             mp3_fp.seek(0)
#             audio = AudioSegment.from_file(mp3_fp, format="mp3")
#             play(audio)

#         # Then stop and release VLC
#         player.stop()
#         # player.release()



# Listen for the wake word "ivy"
def listen_for_wake_word(source):
    # # Setup the system message for the GPT
    # messages = [{"role": "system",
    #              "content": "You are a helpful personal assistant. Try to answer the questions in 20 words or less"}]

    print("Listening for 'ivy'...")

    # r.adjust_for_ambient_noise(source, duration=0.5)

    while True:
        # close_player_if_ended(player)
        audio = r.listen(source) #, timeout=10, phrase_time_limit=30)
        # DEBUG: show length of recording in seconds
        # duration = len(audio.frame_data) / audio.sample_rate / 2  # divide by 2 for 16-bit samples
        # print(f"[DEBUG] Captured audio duration: {duration:.2f} seconds")
        try:
            text = r.recognize_google(audio) # Trade back voice model
            if "ivy" in text.lower():
                print("Wake word detected.")
                # pause_if_playing(player)

                playsound(listen_chime)
                if tts_engine == 'pyttsx3':
                    engine.say(np.random.choice(greetings))
                    engine.runAndWait()
                else:
                    # greet = gTTS(text=np.random.choice(greetings), lang=language)
                    # greet.save('response.mp3')
                    # playsound('response.mp3')
                    tts = gTTS(text=np.random.choice(greetings), lang=language)
                    mp3_fp = io.BytesIO()
                    tts.write_to_fp(mp3_fp)
                    mp3_fp.seek(0)

                    audio = AudioSegment.from_file(mp3_fp, format="mp3")
                    play(audio)
                listen_and_respond(source,messages)
                break
        # except sr.UnknownValueError:
        #     pass
        # except sr.RequestError as e:
        #     print(f"Google Speech API request failed during wake word listening: {e}")
        # except TimeoutError as e:
        #     print(f"Network timeout during wake word listening: {e}")       
        except sr.UnknownValueError:
            # Handle unrecognized speech: just continue listening without breaking
            print("Could not understand audio, listening again...")
            # play_if_paused(player)
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            # Optionally break or continue depending on severity
            break

# def listen_full_utterance(recognizer, source, timeout=10):
#     print("Listening (full utterance)...")
#     return recognizer.listen(source, timeout=timeout)

# def listen_until_silence(recognizer, source, max_duration=10, silence_threshold=1.0):
#     print("Listening (custom)...")
#     audio_segments = []
#     start_time = time.time()
#     last_sound_time = time.time()

#     while True:
#         try:
#             # Listen in short chunks
#             chunk = recognizer.listen(source, timeout=1, phrase_time_limit=3)
#             audio_segments.append(chunk.get_raw_data())
#             last_sound_time = time.time()
#         except sr.WaitTimeoutError:
#             # No input detected in 1 second
#             if time.time() - last_sound_time > silence_threshold:
#                 break
#         except Exception as e:
#             print(f"[DEBUG] Listen chunk error: {e}")
#             break

#         if time.time() - start_time > max_duration:
#             print("[DEBUG] Max recording time reached.")
#             break

#     if not audio_segments:
#         return None

#     combined_audio = b''.join(audio_segments)
#     return sr.AudioData(combined_audio, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

# Listen for input and respond with OpenAI API
def listen_and_respond(source, messages):
    global vlc_process
    while True:
        print("Listening...")
        try:
            # r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=15, phrase_time_limit=10)#, phrase_time_limit=20)
            # audio = listen_full_utterance(r, source)
            # DEBUG: show length of recording in seconds
            # duration = len(audio.frame_data) / audio.sample_rate / 2  # divide by 2 for 16-bit samples
            # print(f"[DEBUG] Captured audio duration: {duration:.2f} seconds")
        except sr.WaitTimeoutError:
            print("No speech detected")
            r.adjust_for_ambient_noise(source, duration=1)
            listen_for_wake_word(source)
            #break
        # print(f'audio len {len(audio)}')
        if audio:
            try:
                text = r.recognize_google(audio)
                # text = recognize_vosk(audio)
                print(f"You said: {text}")
                if not text:
                    r.adjust_for_ambient_noise(source, duration=1)
                    listen_for_wake_word(source)
                    # continue 
                else:
                    lower_text = text.lower()
                    ### Weather Logic Branch ###
                    if "play" in lower_text:
                        # video_title = lower_text.rsplit(' ',1)[-1]
                        video_title = lower_text.split()[-2] if lower_text.endswith("video") else lower_text.split()[-1]
                        print(f'Video title {video_title}')
                        matched_filename = find_one_video_filename_with_string(video_title, directory_path)
                        if matched_filename:
                            print("Found:", matched_filename)
                            response_text = "Found file" + matched_filename + "playing..."
                            full_file_path = os.path.join(directory_path, matched_filename)
                            vlc_process = subprocess.Popen([vlc_path,"--fullscreen",full_file_path])
                            # play_video = instance.media_new(directory_path + "/" + matched_filename)
                            # player.set_media(play_video)
                            # player.play()
                            # time.sleep(1)
                            #Done
                            # listen_for_wake_word(source)
                            # player.set_fullscreen(True)
                        else:
                            print("No match found")
                            response_text = "No file found, tell me again what to play?"
                    elif "pause" in lower_text:
                        # # pause_if_playing(player)
                        # time.sleep(2)  # wait for VLC to open
                        pyautogui.press("space")  # space bar toggles pause/play    
                        response_text = "Pausing video"
                    elif "resume" in lower_text:
                        pyautogui.press("space")  # space bar toggles pause/play    
                        response_text = "Resuming video"                        
                    elif "stop" in lower_text:
                        # pause_if_playing(player)
                        pyautogui.press("space")  # space bar toggles pause/play                            
                        response_text = "Pausing video"
                    # elif "resume" in lower_text:
                    #     play_if_paused(player)
                    #     response_text = "resuming video"
                    elif "close" in lower_text:
                        # close_vlc_player(player)  
                        if vlc_process:
                            vlc_process.terminate()  # nicely closes VLC
                            vlc_process = None
                            response_text = "closing video"
                        else:
                            response_text = "No video is currently playing"

                    # elif "current weather" in lower_text:
                    #     response_text = get_current_weather_open_meteo()

                    # elif "next 7 days" in lower_text or "weekly weather" in lower_text or "weather this week" in lower_text:
                    #     response_text = get_weekly_weather_open_meteo()
                    else:
                        # Default: send to OpenAI
                        # messages.append({'role': 'user', 'content': text})
                        # response_text = get_completion(messages)
                        # messages.append({'role': 'assistant', 'content': response_text})
                        # response_text = lower_text
                        response_text = ' '
                        # continue

                    # messages.append({'role':'user', 'content':text})

                    # Send input to OpenAI API
                    # response_text = get_completion(messages)
                    print(response_text)

                    if tts_engine == 'pyttsx3':
                        engine.say(response_text)
                        engine.runAndWait()

                    elif tts_engine == 'gtts':
                        # resp = gTTS(text=response_text, lang=language)
                        # resp.save('response2.mp3')
                        # playsound('response2.mp3')
                        # os.remove('response2.mp3')
                        if response_text.strip():
                            tts = gTTS(text=response_text, lang=language)
                            mp3_fp = io.BytesIO()
                            tts.write_to_fp(mp3_fp)
                            mp3_fp.seek(0)

                            audio = AudioSegment.from_file(mp3_fp, format="mp3")
                            play(audio)
                        else:
                            print("No response_text to speak.")

                    elif tts_engine == 'openai':
                        response = client.audio.speech.create(
                            model="tts-1",
                            voice="alloy",
                            input=response_text
                            )

                        # response.stream_to_file('response.mp3')
                        # # Speak the response
                        # print("speaking")
                        # playsound('response.mp3')
                        output_file = Path("response2.mp3")
                        with open(output_file, "wb") as f:
                            for chunk in response.with_streaming_response().iter_bytes():
                                f.write(chunk)

                        print("speaking")
                        playsound(str(output_file))

                    # Append the response to the response list
                    # messages.append({'role':'assistant', 'content':response_text})

                    # playsound("listen_chime.mp3")

                    if not audio:
                        playsound("error.mp3")
                        print("error audio")
                        listen_for_wake_word(source)

            except sr.UnknownValueError:
                # playsound("error.mp3")
                print("Silence found, shutting up, listening...")
                playsound(end_chime)
                # os.remove('response.mp3')
                #clear background noise
                # play_if_paused(player)
                time.sleep(0.5)
                r.adjust_for_ambient_noise(source, duration=1)#0.5)
                listen_for_wake_word(source)
                break

            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                engine.say(f"Could not request results; {e}")
                engine.runAndWait()
                # play_if_paused(player)
                listen_for_wake_word(source)
                break

def find_one_video_filename_with_string(search_str, directory, video_extensions=None):
    if video_extensions is None:
        video_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv']
    
    search_lower = search_str.lower()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename_lower = file.lower()
            if any(filename_lower.endswith(ext) for ext in video_extensions):
                if search_lower in filename_lower:
                    return file  # return first match immediately
    
    return None  # if no match found

##MAIN##
#Start audio
# Use the default microphone as the audio source
with sr.Microphone() as source:
# with sr.Microphone(sample_rate=16000) as source:
    r.adjust_for_ambient_noise(source, duration=1)
    listen_for_wake_word(source)