from playsound import playsound


class AudioPlayer:

    def play(
        self,
        audio_path: str
    ):

        playsound(audio_path)