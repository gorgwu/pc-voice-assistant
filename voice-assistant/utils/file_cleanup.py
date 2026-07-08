import os
import glob


def clean_recordings(folder="recordings"):

    if not os.path.exists(folder):
        return

    files = glob.glob(os.path.join(folder, "*.mp3"))

    for f in files:

        try:
            os.remove(f)
        except Exception as e:
            print(f"Could not delete {f}: {e}")