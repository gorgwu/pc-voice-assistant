import os
from typing import Any, Dict, List

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:  # pragma: no cover - handled at runtime
    spotipy = None
    SpotifyOAuth = None


class SpotifyClient:

    SCOPES = [
        "user-read-playback-state",
        "user-modify-playback-state",
        "user-read-currently-playing"
    ]

    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", "")
        self.username = os.getenv("SPOTIFY_USERNAME", "")
        self.auth_manager = None
        self.client = None

    def is_configured(self) -> bool:
        return bool(
            self.client_id
            and self.client_secret
            and self.redirect_uri
            and self.username
        )

    def _ensure_workspace(self) -> None:
        os.makedirs("workspace", exist_ok=True)

    def _build_auth_manager(self):
        if not self.is_configured():
            raise RuntimeError(
                "Spotify credentials are missing. Set SPOTIFY_CLIENT_ID, "
                "SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, and SPOTIFY_USERNAME."
            )

        if SpotifyOAuth is None:
            raise RuntimeError("spotipy is not installed. Install it with pip install spotipy")

        self._ensure_workspace()

        self.auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=" ".join(self.SCOPES),
            username=self.username,
            open_browser=False,
            show_dialog=False,
            cache_path=os.path.join("workspace", ".spotify_cache")
        )

        return self.auth_manager

    def get_client(self):
        if spotipy is None:
            raise RuntimeError("spotipy is not installed. Install it with pip install spotipy")

        if self.client is None:
            auth_manager = self.auth_manager or self._build_auth_manager()
            self.client = spotipy.Spotify(auth_manager=auth_manager)

        return self.client

    def search_tracks(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not query or not query.strip():
            return []

        client = self.get_client()
        results = client.search(q=query, type="track", limit=limit)

        tracks = []
        for item in results.get("tracks", {}).get("items", []):
            artists = item.get("artists") or []
            tracks.append({
                "name": item.get("name"),
                "artist": artists[0].get("name") if artists else "Unknown artist",
                "id": item.get("id"),
                "uri": item.get("uri"),
                "preview_url": item.get("preview_url")
            })

        return tracks

    def play_track(self, query: str) -> Dict[str, Any]:
        tracks = self.search_tracks(query, limit=1)
        if not tracks:
            raise RuntimeError(f"No Spotify track found for query: {query}")

        track = tracks[0]
        client = self.get_client()
        client.start_playback(uris=[track["uri"]])

        return {
            "status": "playing",
            "name": track["name"],
            "artist": track["artist"],
            "uri": track["uri"]
        }

    def pause_playback(self) -> Dict[str, Any]:
        client = self.get_client()
        client.pause_playback()
        return {"status": "paused"}

    def resume_playback(self) -> Dict[str, Any]:
        client = self.get_client()
        client.start_playback()
        return {"status": "resumed"}

    def get_current_track(self) -> Dict[str, Any]:
        client = self.get_client()
        result = client.current_user_playing_track()
        if not result or not result.get("item"):
            return {"status": "nothing_playing"}

        item = result["item"]
        artists = item.get("artists") or []
        return {
            "status": "playing",
            "name": item.get("name"),
            "artist": artists[0].get("name") if artists else "Unknown artist",
            "id": item.get("id")
        }

    def create_playlist(self, name: str, description: str = "") -> Dict[str, Any]:
        client = self.get_client()
        user = client.current_user()["id"]
        playlist = client.user_playlist_create(
            user=user,
            name=name,
            public=False,
            description=description
        )

        return {
            "status": "created",
            "name": playlist.get("name"),
            "id": playlist.get("id"),
            "url": playlist.get("external_urls", {}).get("spotify")
        }
