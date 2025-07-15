# VLC Voice Assistant 🎙️🎶

A voice-controlled assistant for VLC Media Player — control playback, volume, and more using simple voice commands.

## 🚀 Getting Started

To use the VLC Voice Assistant:

1. **Download the executable**  
   Go to the [`dist/`](./dist) folder and download the `.exe` file.

2. **Follow the instructions**  
   After downloading, open the `INSTRUCTIONS.txt` file and follow the steps to get started.

---

## 🐍 For Developers / Running from Source

If you want to run or modify the assistant from source code, follow these steps:

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # On Windows (cmd):
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Generate or update `requirements.txt`** (after installing new packages):

   ```bash
   pip freeze > requirements.txt
   ```

4. **Optional compile to exe**
   `pip install pyinstaller`
   - See COMPILE.txt file

---

## 📁 Project Structure

```
├── build/              # Compiled .exe file lives here
├── INSTRUCTIONS.txt    # Step-by-step usage guide
├── requirements.txt    # Python dependencies
├── vlc_assistant.py    # Python source code
└── README.md           # This file
```

## 💡 Features

- Voice command support for VLC controls like:
  - Play _\<description that is in the name of a video\>_
  - Pause, Stop, Resume, Close active video

## 🛠️ Built With

- Python 3
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [gTTS](https://pypi.org/project/gTTS/)
- [VLC Python bindings](https://pypi.org/project/python-vlc/)

---

Thanks for checking it out! If you like it, consider starring the repo ⭐
