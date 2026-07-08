import json

from tools.base_tool import BaseTool
from utils.spotify_client import SpotifyClient


class SpotifySearchTrackTool(BaseTool):

    name = "spotify_search_track"
    description = """
    Search Spotify for tracks.

    Arguments:
    - query
    """

    def run(self, arguments: dict):
        query = arguments["query"]
        client = SpotifyClient()
        results = client.search_tracks(query)
        return json.dumps(results)
