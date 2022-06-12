import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


# This is an association table, it stores info about relationships.
post_thread = db.Table(
    "post_thread",
    db.metadata, # Pure unadulterated magic.
    db.Column("parent_post_id", db.Integer, db.ForeignKey('post.id')),
    db.Column("child_post_id", db.Integer, db.ForeignKey('post.id')),
)


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=True)
    body = db.Column(db.Text, nullable=True)
    child = db.relationship(
        "Post",
        secondary=post_thread,
        primaryjoin=(id == post_thread.c.parent_post_id),
        secondaryjoin=(id == post_thread.c.child_post_id),
        backref=db.backref("parent", lazy="joined"),
        uselist=False
    )

    def __repr__(self):
        return """<Post: {}>""".format(self.title)

    def serialize(self):
        if self.child:
            child_url = "".join([
                os.getenv("BACKEND_URL"),
                "/api/post/",
                str(self.child.id)
            ])
        else:
            child_url = None
        
        if len(self.parent):
            parent_url = "".join([
                os.getenv("BACKEND_URL"),
                "/api/post/",
                str(self.parent[0].id)
            ])
        else:
            parent_url = None

        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "links": {
                "prev": parent_url,
                "next": child_url
            }
        }
