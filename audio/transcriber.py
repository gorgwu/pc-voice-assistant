import time

from google import genai

from config import (
    GEMINI_API_KEY,
    MODEL_NAME
)


class AudioTranscriber:

    MAX_RETRIES = 3

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def transcribe(
        self,
        audio_path: str
    ):

        audio_file = (
            self.client.files.upload(
                file=audio_path
            )
        )

        for attempt in range(
            self.MAX_RETRIES
        ):

            try:

                response = (
                    self.client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[
                            (
                                "Transcribe this "
                                "audio recording "
                                "exactly."
                            ),
                            audio_file
                        ]
                    )
                )

                return response.text

            except Exception as e:

                print(
                    f"\nTranscription failed "
                    f"(attempt "
                    f"{attempt + 1}/"
                    f"{self.MAX_RETRIES})"
                )

                print(e)

                if (
                    attempt
                    ==
                    self.MAX_RETRIES - 1
                ):

                    raise e

                print(
                    "\nRetrying in 5 seconds..."
                )

                time.sleep(5)