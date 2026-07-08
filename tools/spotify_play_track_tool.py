from tools.base_tool import BaseTool
from utils.spotify_client import SpotifyClient


class SpotifyPlayTrackTool(BaseTool):

    name = "spotify_play_track"
    description = """
    Play a Spotify track by search query.

    Arguments:
    - query
    """

    def run(self, arguments: dict):
        query = arguments["query"]
        client = SpotifyClient()
        return client.play_track(query)
