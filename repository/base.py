from web import db
from datetime import datetime
from abc import abstractmethod


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def before_save(self):
        pass

    def after_save(self):
        pass

    def save(self):
        self.before_save()
        db.session.add(self)
        db.session.commit()
        self.after_save()

    def before_delete(self):
        pass

    def after_delete(self):
        pass

    def delete(self):
        self.before_delete()
        db.session.delete(self)
        db.session.commit()
        self.after_delete()

    def before_update(self):
        pass

    def after_update(self):
        pass

    def update(self, **kwargs):
        self.before_update()
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        self.after_update()

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
