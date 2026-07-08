from tools.base_tool import BaseTool
from utils.spotify_client import SpotifyClient


class SpotifyGetCurrentTrackTool(BaseTool):

    name = "spotify_get_current_track"
    description = """
    Get the currently playing Spotify track.
    """

    def run(self, arguments: dict):
        client = SpotifyClient()
        return client.get_current_track()
