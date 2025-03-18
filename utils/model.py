class Result:
    def __init__(self, song_id: str, track_name: str, album_name: str, artist: str, image_url: str, song_url: str, result: int) -> None:
        self.song_id = song_id
        self.track_name = track_name
        self.album_name = album_name
        self.artist = artist
        self.image_url = image_url
        self.song_url = song_url
        self.result = result

    def to_json(self) -> dict:
        return {
            "song_id": self.song_id,
            "track_name": self.track_name,
            "album_name": self.album_name,
            "artist": self.artist,
            "image_url": self.image_url,
            "song_url": self.song_url,
            "result": self.result,
        }
