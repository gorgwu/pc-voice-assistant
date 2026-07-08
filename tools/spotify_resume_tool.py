from tools.base_tool import BaseTool
from utils.spotify_client import SpotifyClient


class SpotifyResumePlaybackTool(BaseTool):

    name = "spotify_resume_playback"
    description = """
    Resume Spotify playback.
    """

    def run(self, arguments: dict):
        client = SpotifyClient()
        return client.resume_playback()
