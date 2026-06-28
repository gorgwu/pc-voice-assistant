import sounddevice as sd
import soundfile as sf
import numpy as np

from config import (
    SAMPLE_RATE,
    CHANNELS,
    RECORDING_PATH
)


class AudioRecorder:

    def __init__(self):

        self.frames = []

        self.stream = None

    def callback(
        self,
        indata,
        frames,
        time,
        status
    ):

        self.frames.append(
            indata.copy()
        )

    def record(self):

        input(
            "\nPress ENTER to start recording..."
        )

        self.frames = []

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=self.callback
        )

        self.stream.start()

        print(
            "Recording... Press ENTER to stop."
        )

        input()

        self.stream.stop()

        self.stream.close()

        audio = np.concatenate(
            self.frames,
            axis=0
        )

        sf.write(
            RECORDING_PATH,
            audio,
            SAMPLE_RATE
        )

        print("Recording saved.")

        return RECORDING_PATH