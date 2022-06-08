"""Models for Tiktok tracking app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user (of my app)."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # created = db.Column(db.DateTime)

    # user.creator available via backref under class Creator 

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Creator(db.Model):
    """A creator (on Tiktok)."""

    __tablename__ = "creators"

    creator_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False)
    # secUid = db.Column(db.String) 

    users = db.relationship("User", secondary="users_creators", backref="creators")

    def __repr__(self):
        return f"<Creator creator_id={self.creator_id} username={self.username}>"


class UserCreator(db.Model):
    """User <> Creator association table."""

    __tablename__ = "users_creators"

    user_creator_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    creator_id = db.Column(db.Integer, db.ForeignKey("creators.creator_id"))
 
    def __repr__(self):
        return f"<Link user_creator_id={self.user_creator_id} user_id={self.user_id} creator_id={self.creator_id}>"


class Metric(db.Model):
    """The metrics."""

    __tablename__ = "metrics"

    metrics_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("creators.creator_id"))
    dl_date = db.Column(db.DateTime, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    following = db.Column(db.Integer, nullable=False)
    videos = db.Column(db.Integer, nullable=False) 
    likes = db.Column(db.Integer, nullable=False)

    creators = db.relationship("Creator", backref="metrics")

    def __repr__(self):
        return f"<Metrics metrics_id={self.metrics_id} creator_id={self.creator_id} dl_date={self.dl_date} followers={self.followers} following={self.following} videos={self.videos} likes={self.likes}>"


def connect_to_db(flask_app, db_uri="postgresql:///metrics", echo=True): 
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
