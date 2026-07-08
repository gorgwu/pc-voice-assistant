from bots.base_bot import BaseBot


class MusicBot(BaseBot):

    capability_tags = ("tools",)
    tool_names = (
        "spotify_search_track",
        "spotify_play_track",
        "spotify_pause_playback",
        "spotify_resume_playback",
        "spotify_get_current_track"
    )

    SYSTEM_PROMPT = """
    You are a music assistant.

    You can use Spotify tools to search tracks, play music, pause or resume playback,
    inspect the current track, and create playlists.

    If a tool is required, respond with ONLY a JSON object.
    Do NOT wrap JSON in markdown.
    Do NOT explain the JSON.
    Do NOT include any text before or after the JSON.

    JSON format:

    {
        "tool": "tool_name",
        "arguments": {}
    }
    """

    def __init__(self):

        super().__init__(
            name="musicbot",
            system_prompt=self.SYSTEM_PROMPT,
            tools=list(self.tool_names)
        )
