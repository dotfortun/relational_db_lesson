"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Post
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/post/<int:id>', methods=["GET"])
def get_post(id):
    post = Post.query.filter_by(id=id).one_or_none()
    if post:
        return jsonify(post.serialize()), 200
    else:
        return jsonify({"msg": "Post doesn't exist"}), 400

@api.route('/posts', methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify(posts=[
        post.serialize() for post in posts
    ]), 200

@api.route("/thread/<int:id>")
def get_thread(id):
    posts = []
    root_post = Post.query.filter_by(id=id).one_or_none()

    if root_post:
        post = root_post
        while len(post.parent):
            if post not in posts:
                posts.append(post)
            post = post.parent[0]
        while post.child:
            if post not in posts:
                posts.append(post)
            post = post.child
        posts.append(post)
        posts.sort(key=lambda x: x.id)
        return jsonify(thread=[post.serialize() for post in posts]), 200
    return jsonify(msg="Thread not found."), 400
