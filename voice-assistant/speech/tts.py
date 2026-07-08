from gtts import gTTS
import os
import time


class TextToSpeech:

    def __init__(self, accent="com"):
        self.accent = accent

    def generate(self, text: str, output_dir="recordings"):

        os.makedirs(output_dir, exist_ok=True)

        filename = f"response_{int(time.time() * 1000)}.mp3"
        path = os.path.join(output_dir, filename)

        tts = gTTS(
            text=text,
            lang="en",
            tld=self.accent
        )

        tts.save(path)

        return path