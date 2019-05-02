from pymongo import MongoClient


# connection to MongoDB Database
connection = MongoClient("mongodb://127.0.0.1:27017/")


# Initialize Database
def create_mongodatabase():
    try:
        dbnames = connection.database_names()
        if 'blog_database' not in dbnames:
            db_authors = connection.blog_database.authors
            db_posts = connection.blog_database.posts
            db_api = connection.blog_database.apirelease

            db_authors.insert({
                "email": "author@domain.com",
                "author_ID": 1,
                "name": "author's name",
                "password": "<secret>",
                "username": "username",
                "bio": "some bio of the author"
            })

            db_posts.insert({
                "post_title": "First Post",
                "post_slug": "first-post",
                "post_created_at": "2018-12-12T17:47:40Z",
                "post_picture": "https://path_to_a_image",
                "post_content": "The first post of the blog, added as a draft",
                "published": False,
                "author_id": 1,
                "post_ID": 1
            })

            db_api.insert({
              "buildtime": "2018-12-11 11:37:00",
              "links": "/info",
              "methods": "get",
              "version": "0.1"
            })
            db_api.insert({
              "buildtime": "2018-12-12 11:50:00",
              "links": "/posts",
              "methods": "get, post, put, delete",
              "version": "0.2"
            })
            print("Database Initialize completed!")
        else:
            print("Database already Initialized!")
    except:
        print("Database creation failed!!")


create_mongodatabase()
