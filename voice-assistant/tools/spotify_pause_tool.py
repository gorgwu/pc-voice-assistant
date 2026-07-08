from tools.base_tool import BaseTool
from utils.spotify_client import SpotifyClient


class SpotifyPausePlaybackTool(BaseTool):

    name = "spotify_pause_playback"
    description = """
    Pause Spotify playback.
    """

    def run(self, arguments: dict):
        client = SpotifyClient()
        return client.pause_playback()
