import os
from gtts import gTTS
from playsound import playsound
from threading import Thread

def delete_directory():
    filelist = [f for f in os.listdir('play') if f.endswith(".mp3")]
    for f in filelist:
        os.remove(os.path.join('play', f))

def speak(data, playcount):
    class PlayThread(Thread):
        def __init__(self, data, playcount):
            super().__init__()
            self.data = data
            self.playcount = playcount

        def run(self):
            t1 = gTTS(text=self.data, lang='en', slow=False)
            path = f"play/{self.playcount}.mp3"
            t1.save(path)
            playsound(path)

    newthread = PlayThread(data, playcount)
    newthread.start()
