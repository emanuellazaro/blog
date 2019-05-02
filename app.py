from flask import Flask, request, jsonify
from flask import abort
from flask import make_response
from flask_cors import CORS
from time import gmtime, strftime
from pymongo import MongoClient
import bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

# connection to MongoDB Database
connection = MongoClient("mongodb://127.0.0.1:27017/")


# Object creation
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '<some secret key>'

CORS(app, origins=['http://127.0.0.1:8080'])
jwt = JWTManager(app) # why use this command?


@app.route("/info/")
def home_index():
    api_list = []
    db = connection.blog_database.apirelease
    for row in db.find():
        row.pop('_id')
        api_list.append(row)
    return jsonify(api_list), 200


@app.route('/posts/', methods=['GET'])
def get_posts():
    return list_posts()
    """Let's define list_posts() function which connects to database and
    get us all the posts and respond back with posts list"""


def list_posts():
    api_list = []
    db = connection.blog_database.posts
    db_authors = connection.blog_database.authors
    for row in db.find({'published': True}):
        row.pop('_id')
        # row.pop('post_content')
        row.pop('published')
        for author in db_authors.find({"author_ID": row['author_id']}):
            row['author_name'] = author['name']
            row['author_bio'] = author['bio']
        row.pop('author_id')
        api_list.append(row)
    return jsonify(api_list), 200


@app.route('/drafts/', methods=['GET'])
def get_drafts():
    return list_drafts()
    """Let's define list_drafts() function which connects to database and
    get us all the drafts and respond back with drafts list"""


def list_drafts():
    api_list = []
    db = connection.blog_database.posts
    db_authors = connection.blog_database.authors
    for row in db.find({'published': False}):
        row.pop('_id')
        # row.pop('post_content')
        row.pop('published')
        for author in db_authors.find({"author_ID": row['author_id']}):
            row['author_name'] = author['name']
            row['author_bio'] = author['bio']
        row.pop('author_id')
        api_list.append(row)
    return jsonify(api_list)


@app.route('/posts/', methods=['POST'])
def add_posts():
    post = {}
    print(request.json)
    if not request.json or not 'author_id' in request.json or not 'post_title' in request.json:
        abort(400)
    post['post_title'] = request.json['post_title']
    slug = request.json['post_title'].lower().replace(" ", "-")
    post['post_slug'] = slug
    post['post_created_at'] = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    post['post_picture'] = request.json['post_picture']
    post['post_content'] = request.json['post_content']
    post['published'] = request.json['published']
    post['author_id'] = request.json['author_id']
    print(post)
    # TODO: get next post_ID and add the value with the post  <<------------------------------------------
    return jsonify({'status': add_post(post)}), 201


def add_post(new_post):
    api_list = []
    db_authors = connection.blog_database.authors
    db_posts = connection.blog_database.posts
    author = db_authors.find({"author_ID": new_post['author_id']})
    for row in author:
        api_list.append(str(row))

    if api_list == []:
        abort(404)
    else:
        db_posts.insert_one(new_post)
        return "Success"


@app.route('/posts/<slug>/', methods=['GET'])
def get_post(slug):
    return get_post_content(slug)


def get_post_content(post_slug):
    db = connection.blog_database.posts
    db_authors = connection.blog_database.authors
    api_list = []
    post = db.find({'post_slug': post_slug})
    for row in post:
        row.pop('_id')
        for author in db_authors.find({"author_ID": row['author_id']}):
            row['author_name'] = author['name']
            row['author_bio'] = author['bio']
        row.pop('author_id')
        api_list.append(row)

    if api_list == []:
        abort(404)

    return jsonify({'post': api_list})


@app.route('/posts/', methods=['DELETE'])
def delete_post():
    if not request.json or not 'slug' in request.json:
        abort(400)
    slug = request.json['slug']
    return jsonify({'status': del_post(slug)}), 200


def del_post(del_post_slug):
    db = connection.blog_database.posts
    api_list = []
    for i in db.find({'post_slug': del_post_slug}):
        api_list.append(str(i))

    if api_list == []:
        abort(404)
    else:
        db.remove({"post_slug": del_post_slug})
        return "Success"


@app.route('/posts/<slug>/', methods=['PUT'])
def update_post(slug):
    post = {}
    if not request.json or not 'slug' in request.json:
        abort(400)
    post['post_slug'] = slug
    key_list = request.json.keys()
    for i in key_list:
        post[i] = request.json[i]
    return jsonify({'status': upd_post(post)}), 200


def upd_post(upd_post):
    api_list = []
    db_posts = connection.blog_database.posts
    post = db_posts.find_one({"post_slug": upd_post['post_slug']})
    for i in post:
        api_list.append(str(i))

    if api_list == []:
        abort(409)
    else:
        new_slug = upd_post['post_title'].lower().replace(" ", "-")
        upd_post['post_slug'] = new_slug
        upd_post['post_updated_at'] = strftime("%m-%d-%Y", gmtime())
        db_posts.update_one({'post_ID': post['post_ID']}, {'$set': upd_post}, upsert=False)
        return "Success"


@app.route('/login', methods=['POST'])
def login():
    authors = connection.blog_database.authors
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = authors.find_one({'email': email})

    if response:
        # if bcrypt.check_password_hash(response['password'], password):
        if response['password'] == password:
            access_token = create_access_token(identity={
                'name': response['name'],
                'author_id': response['author_ID'],
                'email': response['email']}
                )
            result = access_token
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result


@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
