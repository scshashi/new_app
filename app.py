from flask import Flask, jsonify, request, abort

app = Flask(__name__)

posts = [
    {"id": 1, "title": "First Post", "body": "This is the first post."},
    {"id": 2, "title": "Second Post", "body": "This is the second post."}
]

comments = [
    {"id": 1, "postId": 1, "name": "Alice", "body": "Great post!"},
    {"id": 2, "postId": 2, "name": "Bob", "body": "Nice work."}
]

albums = [
    {"id": 1, "title": "First Album", "userId": 1},
    {"id": 2, "title": "Second Album", "userId": 2}
]

# helper functions

def get_next_id(collection):
    return max((item["id"] for item in collection), default=0) + 1


def find_item(collection, item_id):
    return next((item for item in collection if item["id"] == item_id), None)


# Posts endpoints

@app.route("/posts", methods=["GET"])
def list_posts():
    return jsonify(posts)


@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = find_item(posts, post_id)
    if not post:
        abort(404)
    return jsonify(post)


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json(force=True)
    if not data or "title" not in data or "body" not in data:
        abort(400)
    new_post = {
        "id": get_next_id(posts),
        "title": data["title"],
        "body": data["body"]
    }
    posts.append(new_post)
    return jsonify(new_post), 201


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = find_item(posts, post_id)
    if not post:
        abort(404)
    data = request.get_json(force=True)
    post["title"] = data.get("title", post["title"])
    post["body"] = data.get("body", post["body"])
    return jsonify(post)


@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = find_item(posts, post_id)
    if not post:
        abort(404)
    posts.remove(post)
    return jsonify({"message": "Post deleted."})


# Comments endpoints

@app.route("/comments", methods=["GET"])
def list_comments():
    return jsonify(comments)


@app.route("/comments/<int:comment_id>", methods=["GET"])
def get_comment(comment_id):
    comment = find_item(comments, comment_id)
    if not comment:
        abort(404)
    return jsonify(comment)


@app.route("/comments", methods=["POST"])
def create_comment():
    data = request.get_json(force=True)
    if not data or "postId" not in data or "name" not in data or "body" not in data:
        abort(400)
    new_comment = {
        "id": get_next_id(comments),
        "postId": data["postId"],
        "name": data["name"],
        "body": data["body"]
    }
    comments.append(new_comment)
    return jsonify(new_comment), 201


@app.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = find_item(comments, comment_id)
    if not comment:
        abort(404)
    data = request.get_json(force=True)
    comment["postId"] = data.get("postId", comment["postId"])
    comment["name"] = data.get("name", comment["name"])
    comment["body"] = data.get("body", comment["body"])
    return jsonify(comment)


@app.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = find_item(comments, comment_id)
    if not comment:
        abort(404)
    comments.remove(comment)
    return jsonify({"message": "Comment deleted."})


# Albums endpoints

@app.route("/albums", methods=["GET"])
def list_albums():
    return jsonify(albums)


@app.route("/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    album = find_item(albums, album_id)
    if not album:
        abort(404)
    return jsonify(album)


@app.route("/albums", methods=["POST"])
def create_album():
    data = request.get_json(force=True)
    if not data or "title" not in data or "userId" not in data:
        abort(400)
    new_album = {
        "id": get_next_id(albums),
        "title": data["title"],
        "userId": data["userId"]
    }
    albums.append(new_album)
    return jsonify(new_album), 201


@app.route("/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    album = find_item(albums, album_id)
    if not album:
        abort(404)
    data = request.get_json(force=True)
    album["title"] = data.get("title", album["title"])
    album["userId"] = data.get("userId", album["userId"])
    return jsonify(album)


@app.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    album = find_item(albums, album_id)
    if not album:
        abort(404)
    albums.remove(album)
    return jsonify({"message": "Album deleted."})


@app.route("/")
def home():
    return jsonify({
        "message": "Flask API is running",
        "routes": ["/posts", "/comments", "/albums"]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
