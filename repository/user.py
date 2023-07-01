from repository.base import BaseModel
from web import db


class User(BaseModel):
    __tablename__ = 'AUTH_USER'

    username = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User: {self.username}>"

    def __str__(self):
        return f"{self.username}"


class Permission(BaseModel):
    __tablename__ = 'AUTH_PERMISSION'

    internal_code = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<Permission: {self.internal_code}>"

    def __str__(self):
        return f"{self.internal_code}"
