import enum
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ResultEnum(enum.Enum):

    FLOP = 0
    HIT = 1


class Results(db.Model):
    __tablename__ = "SongsavvyResults"
    id = db.Column(db.String(22), primary_key=True)
    track_name = db.Column(db.String(100))
    album_name = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    image_url = db.Column(db.String(150))
    song_url = db.Column(db.String(150))
    result = db.Column(Enum(ResultEnum), default=ResultEnum.FLOP)

    def __repr__(self) -> str:
        return f"SongSavvy Result ({self.id}, {self.track_name}, {self.album_name}, {self.artist}, {self.result})"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "trackName": self.track_name,
            "album": self.album_name,
            "artist": self.artist,
            "imgUrl": self.image_url,
            "songUrl": self.song_url,
            "result": self.result.value,
        }
