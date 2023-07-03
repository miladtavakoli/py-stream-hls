from repository.base import BaseModel
from repository.user import User
from web import db


class Movie(BaseModel):
    __tablename__ = 'FILE_MOVIE'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship("User", back_populates='movies')
    hls_filename = db.Column(db.String(250), nullable=True)
    thumbnail = db.Column(db.String(250), nullable=True)
    original_filename = db.Column(db.String(400), nullable=True)
    directory_path = db.Column(db.String(250), nullable=True)
    title = db.Column(db.String(400), nullable=False)
    slug = db.Column(db.String(400), nullable=False, unique=False)
    description = db.Column(db.String(600), nullable=True)
    imdb_tag = db.Column(db.String(40), nullable=True)
    hash_value = db.Column(db.String(64), nullable=True)
    is_private = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Movies: {self.slug}>"

    def __str__(self):
        return f"{self.slug}"
