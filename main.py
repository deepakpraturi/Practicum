import datetime
import json, os
import urllib
from time import sleep

import requests
from google.appengine.ext import ndb
from google.appengine.api import images
from flask import Flask, render_template, Response, request, redirect, url_for

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = '12345'
CORS(app)


class Users(ndb.Model):
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty()
    full_name = ndb.StringProperty(required=True)
    mobile_number = ndb.StringProperty()
    dob = ndb.StringProperty()
    blob = ndb.BlobProperty()
    mimetype = ndb.StringProperty()
    gender = ndb.StringProperty()
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    interested_categories = ndb.StringProperty(repeated=True)
    users_status = ndb.BooleanProperty(required=True, default=True)
    user_type = ndb.StringProperty(default='email')


class Categories(ndb.Model):
    category_name = ndb.StringProperty(required=True)
    category_description = ndb.StringProperty()
    blob = ndb.BlobProperty()
    mimetype = ndb.StringProperty()
    category_status = ndb.BooleanProperty(required=True)


class Posts(ndb.Model):
    # post_id = ndb.StringProperty(required=True)
    post_title = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    category_name = ndb.StringProperty(required=True)
    post_description = ndb.StringProperty()
    post_list = ndb.StringProperty(repeated=True)
    liked_posts = ndb.StringProperty(repeated=True)
    created_date = ndb.DateTimeProperty(required=True, auto_now_add=True)
    post_status = ndb.BooleanProperty(required=True, default=True)
    post_tags = ndb.StringProperty(repeated=True)


class Comments(ndb.Model):
    post_id = ndb.StringProperty(required=True)
    posted_by = ndb.StringProperty(required=True)
    comment_by = ndb.StringProperty()
    comment = ndb.StringProperty()
    comment_date = ndb.DateTimeProperty(auto_now_add=True)
    comment_status = ndb.BooleanProperty(default=True)


class Movies(ndb.Model):
    movie_names = ndb.StringProperty()
    weight = ndb.FloatProperty()


@app.route('/')
def homepage():
    # print(g.user)
    categories = Categories.query().fetch()
    posts = Posts.query().order(-Posts.created_date).fetch()
    return render_template('homepage.html', categories=categories, posts=posts)


@app.before_request
def before_request():
    g.user = None
    g.admin = None
    if 'user' in session:
        g.user = session['user']
    elif 'admin' in session:
        g.admin = session['admin']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        gender = request.form['gender']
        mobile_number = request.form['mobile_number']
        dob = request.form['date']
        print dob
        mimetype = ""
        blob = ""
        user_info = Users(email=email, password=password, full_name=full_name, gender=gender,
                          mobile_number=mobile_number, dob=dob,
                          blob=blob, mimetype=mimetype)
        user_info.put()
        sleep(1.00)
        session['user'] = email
        categories = Categories.query(Categories.category_status == True).fetch()
        return render_template('signup-interested.html', categories=categories)


@app.route('/signup-interested', methods=['GET', 'POST'])
def interested_categories():
    if request.method == 'GET' and g.user:
        categories = Categories.query(Categories.category_status == True).fetch()
        return render_template('signup-interested.html', categories=categories)
    interested_list = request.form.getlist('category')
    key = Users.query(Users.email == session['user']).get()
    key.interested_categories = interested_list
    key.put()
    sleep(1.00)
    return redirect(url_for('user_home'))


@app.route('/ajax-email-check', methods=['POST'])
def email_check():
    email = request.form['email']
    query_email = Users.query(Users.email == email).fetch()
    if len(query_email) >= 1:
        print("success")
        return jsonify({'result': True})
    else:
        print("error")
        return jsonify({'result': False})


@app.route('/ajax-login-check', methods=['POST'])
def login_check():
    print('ajax login check')
    email = request.form['email']
    password = request.form['password']
    query_authenticate = Users.query(Users.email == email).fetch()
    print(query_authenticate)
    if len(query_authenticate) >= 1:
        print(query_authenticate)
        print(query_authenticate[0].password)
        if query_authenticate[0].password == password:
            session['user'] = email
            return jsonify({'result': True})
        else:
            print('Not authenticated')
            return jsonify({'result': False})
    else:
        print('Not authenticated')
        return jsonify({'result': False})


@app.route('/user-home', methods=['GET', 'POST'])
def user_home():
    if request.method == 'GET':
        print('in user home')
        # movies = Movies.query(Movies.movie_names == 'Hello').fetch()
        # if len(movies) > 0:
        #     key = Movies.query(Movies.movie_names == 'Hello').get()
        #     key.weight = 1000
        #     key.put()
        # movies = Movies.query().fetch()
        # print(movies)
        categories = Categories.query(Categories.category_status == True).fetch()
        int_categories = Users.query(Users.email == session['user']).fetch()
        int_categories = int_categories[0].interested_categories
        posts = Posts.query(Posts.post_status == True).fetch()
        post_list = []
        for p in posts:
            if p.category_name in int_categories:
                post_list.append(p)
        return render_template('user-home.html', categories=categories, post_list=post_list)


@app.route('/user-profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'GET':
        user = Users.query(Users.email == session['user']).order(-Users.created_date).fetch()
        posts = Posts.query(Users.email == session['user']).order(-Posts.created_date).fetch()
        categories = Categories.query().fetch()
        return render_template('user-profile.html', user=user, posts=posts, categories=categories)


@app.route('/user-edit-profile', methods=['GET', 'POST'])
def user_edit_profile():
    if request.method == 'POST':
        email = request.args.get('email')
        user = Users.query(Users.email == email).fetch()
        categories = Categories.query(Categories.category_status == True).fetch()
        posts = Posts.query().fetch()
        liked_posts = []
        for p in posts:
            if email in p.liked_posts:
                liked_posts.append(p)
        return render_template('user-edit-profile.html', user=user, categories=categories, liked_posts=liked_posts)


@app.route('/user-update-profile', methods=['GET', 'POST'])
def user_update_profile():
    if request.method == 'POST':
        print('in user update profile')
        email = request.form['email']
        email1 = request.form['email1']
        print email
        key = Users.query(Users.email == email).get()
        key.full_name = request.form['fullname']
        key.mobile_number = request.form['mobile_number']
        key.dob = request.form['date']
        key.interested_categories = request.form.getlist('category')
        key.put()
        sleep(1.00)
        return redirect(url_for('user_home'))


@app.route('/user-update-profile-image', methods=['GET', 'POST'])
def user_update_profile_image():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        return render_template('user-update-profile-image.html', user_id=user_id)
    else:
        user = Users.query(Users.email == session['user']).order(-Users.created_date).fetch()
        posts = Posts.query(Users.email == session['user']).order(-Posts.created_date).fetch()

        user_id = request.args.get('user_id')
        uploaded_file = request.files.get('file')
        if request.files.get('file', None):
            mimetype = uploaded_file.mimetype
            image_data = uploaded_file.stream.read()
            blob = images.resize(image_data, 500, 500)
        else:
            mimetype = ""
            image_data = ""
            blob = ""
        users = Users.query().fetch()
        p = ""
        for user in users:
            if user.key.id() == int(user_id):
                p = user
        p.mimetype = mimetype
        p.image_data = image_data
        p.blob = blob
        p.put()
        return redirect(url_for('user_profile', user=user, posts=posts))


@app.route('/user-delete-profile-image', methods=['POST'])
def user_delete_profile_image():
    if request.method == 'POST':

        user_id = request.args.get('user_id')
        uploaded_file = request.files.get('file')
        mimetype = ""
        blob = ""
        users = Users.query().fetch()
        p = ""
        for user in users:
            if user.key.id() == int(user_id):
                p = user
        p.mimetype = mimetype
        p.blob = blob
        p.put()
        user = Users.query(Users.email == session['user']).order(-Users.created_date).fetch()
        posts = Posts.query(Users.email == session['user']).order(-Posts.created_date).fetch()
        return redirect(url_for('user_profile', user=user, posts=posts))


@app.route('/user-edit-my-post', methods=['GET', 'POST'])
def user_edit_my_post():
    if request.method == 'GET':
        id = request.args.get('post_id')
        post_id = ndb.Key(urlsafe=id)
        post = post_id.get()
        email = session['user']
        categories = Categories.query().fetch()
        return render_template('user-edit-my-post.html', categories=categories, post=post)
    if request.method == 'POST':
        id = request.args.get('post_id')
        post_id = ndb.Key(urlsafe=id)
        post = post_id.get()
        post.post_title = request.form['post_title']
        post.category_name = request.form['selected_category']
        post.post_list = request.form.getlist('list')
        post.put()
        user = Users.query(Users.email == session['user']).order(-Users.created_date).fetch()
        posts = Posts.query(Users.email == session['user']).order(-Posts.created_date).fetch()
        return redirect(url_for('user_profile', user=user, posts=posts))


@app.route('/user-delete-my-post', methods=['GET', 'POST'])
def user_delete_my_post():
    if request.method == 'POST':
        print "In Delete Post"
        id = request.args.get('post_id')
        post_id = ndb.Key(urlsafe=id)
        print post_id.id()
        ndb.Key(Posts, int(post_id.id())).delete()
        sleep(1.00)
        user = Users.query(Users.email == session['user']).order(-Users.created_date).fetch()
        posts = Posts.query(Users.email == session['user']).order(-Posts.created_date).fetch()
        return redirect(url_for('user_profile', user=user, posts=posts))


@app.route('/user-delete-liked-post', methods=['POST'])
def user_delete_liked_post():
    if request.method == 'POST':
        email = session['user']
        post_id = request.args.get('post_id')
        posts = Posts.query().fetch()
        result = []
        for p in posts:
            if p.key.id() == int(post_id):
                print p.liked_posts
                if email in p.liked_posts:
                    result = p.liked_posts
                    result.remove(email)
                    p.liked_posts = result
                    p.put()
                    sleep(1.00)
        return redirect(url_for('user_home'))


@app.route('/view-posts-by-category', methods=['GET', 'POST'])
def view_posts_by_category():
    if request.method == 'GET':
        category_name = request.args.get('category_name')
        post_list = Posts.query(Posts.category_name == category_name).fetch()
        return render_template('view-posts-by-category.html', post_list=post_list)


@app.route('/create-category', methods=['GET', 'POST'])
def create_category():
    if request.method == 'GET':
        categories = Categories.query().fetch()
        return render_template('create-category.html', categories=categories)
    elif request.method == 'POST':
        category_name = request.form['category_name']
        category_description = request.form['category_description']
        uploaded_file = request.files.get('file')
        if request.files.get('file', None):
            mimetype = uploaded_file.mimetype
            image_data = uploaded_file.stream.read()
            blob = images.resize(image_data, 500, 500)
        else:
            mimetype = ""
            image_data = ""
            blob = ""
        cat = Categories(category_name=category_name, category_status=True, category_description=category_description,
                         blob=blob, mimetype=mimetype)
        categories = Categories.query().fetch()
        cat.put()
        sleep(1.00)
        return redirect(url_for('create_category', categories=categories))


@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'GET':
        categories = Categories.query(Categories.category_status == True).fetch()
        return render_template('create-post.html', categories=categories)
    else:
        print('in ajax create post')
        title = request.json['post_title']
        # title = request.form['post_title']
        print(title)
        category_name = request.json['category']
        # category_name = request.form.get('selected')
        print(category_name)
        description = request.json['description']
        print(description)
        email = session['user']
        print(email)
        list1 = request.json['top10']
        # list1 = request.form.getlist('list')
        print(list1)
        tags = []
        # tags = request.form.getlist('tags')
        tags = request.json['tags']
        print(tags)
        tags = tags.split('close')
        # tags = tags.pop(len(tags)-1)
        print(tags)
        posts = Posts(post_title=title, email=email, category_name=category_name,
                      post_description=description, post_list=list1, post_status=True, post_tags=tags)
        posts.put()
        if category_name == 'Music':
            for index, top in enumerate(list1):
                movies = Movies.query(Movies.movie_names == top).fetch()
                if len(movies) > 0:
                    key = Movies.query(Movies.movie_names == top).get()
                    key.weight = key.weight + 10 - index
                    key.put()
                else:
                    new_movie = Movies(movie_names=top, weight=10 - index)
                    new_movie.put()
        return jsonify(posts.key.id())
        # categories = Categories.query(Categories.category_status == True).fetch()
        # return redirect(url_for('create_post', categories=categories))


@app.route('/img/<id>')
def serve_image(id):
    image_key = ndb.Key(urlsafe=id)
    image = image_key.get()
    print image
    return Response(image.blob, mimetype=image.mimetype)


@app.route('/img/email-serve-image', methods=['GET', 'POST'])
def email_serve_image():
    email = request.args.get('email')
    user = Users.query(Users.email == email).fetch()
    print user
    return Response(user[0].blob, mimetype=user[0].mimetype)


@app.route('/post-page', methods=['GET', 'POST'])
def post_page():
    if request.method == 'GET':
        post_id = request.args.get('post_id')
        post = []
        t = Posts.query().fetch()
        for p in t:
            if int(p.key.id()) == int(post_id):
                post.append(p)
        comments = []
        if g.user:
            if session['user'] in post[0].liked_posts:
                like_status = False
            else:
                like_status = True
            comment_status = False
            res_comments = Comments.query().order(Comments.comment_date).fetch()
            print res_comments
            if len(res_comments) > 0:
                for c in res_comments:
                    if int(c.post_id) == post[0].key.id():
                        comments.append(c)
                        comment_status = True
            return render_template('post-page.html', post=post, like_status=like_status, comments=comments,
                                   comment_status=comment_status)
        else:
            return render_template('post-page.html', post=post)


@app.route('/comment-post', methods=['POST'])
def comment_post():
    if request.method == 'POST':
        print('in comment-post post method')
        comment = request.json['comment']
        print('comment = ' + comment)
        comment_by = session['user']
        print('comment by = ' + comment_by)
        post_id = request.json['id']
        print('post-id = ' + post_id)
        posted_by = request.json['posted_by']
        print('posted by = ' + posted_by)
        comment_object = Comments(post_id=post_id, posted_by=posted_by, comment=comment, comment_by=comment_by,
                                  comment_status=True)
        comment_object.put()
        print(comment_object.key.id())
        # sleep(1.00)
        return jsonify(True, session['user'], comment, comment_object.key.id())
        # return redirect(url_for('post_page', post_id=post_id))


@app.route('/delete-comment', methods=['POST'])
def delete_comment():
    if request.method == 'POST':
        print('in delete comment post method')
        comment_id = request.json['comment_id']
        # post_id = request.args.get('post_id')
        print comment_id
        ndb.Key(Comments, int(comment_id)).delete()
        return jsonify(True)
        # return redirect(url_for('post_page', post_id=post_id))


@app.route('/like-post', methods=['POST'])
def like_post():
    if request.method == 'POST':
        posts = Posts.query().fetch()
        like_status = request.json['status']
        print(like_status)
        id = request.json['id']
        print(id)
        post_id = ndb.Key(urlsafe=id)
        post = post_id.get()
        print(post)
        if like_status:
            print "Liking Post"
            liked_list = []
            liked_list = post.liked_posts
            if not session['user'] in liked_list:
                liked_list.append(session['user'])
                print liked_list
                post.liked_posts = liked_list
                post.put()
            return jsonify('liked', len(post.liked_posts))
        else:
            print "Unliking Post"
            liked_list = []
            liked_list = post.liked_posts
            liked_list.remove(session['user'])
            print liked_list
            post.liked_posts = liked_list
            post.put()
            return jsonify('un-liked', len(post.liked_posts))
        # return redirect(url_for('user_home'))


# Admin Pages

@app.route('/admin-home', methods=['GET', 'POST'])
def admin_home():
    if session['admin']:
        if request.method == 'GET':
            users = Users.query().fetch()
            posts = Posts.query().fetch()
            categories = Categories.query().fetch()
            print categories
            return render_template('admin-home.html', users=users, posts=posts, categories=categories)


@app.route('/admin-edit-user', methods=['GET', 'POST'])
def admin_edit_user():
    if session['admin']:
        if request.method == 'POST':
            email = request.args.get('email')
            user = Users.query(Users.email == email).fetch()
            categories = Categories.query(Categories.category_status == True).fetch()
            return render_template('admin-edit-user.html', user=user, categories=categories)


@app.route('/admin-update-user', methods=['GET', 'POST'])
def admin_update_user():
    if session['admin']:
        if request.method == 'POST':
            email = request.form['email']
            key = Users.query(Users.email == email).get()
            key.full_name = request.form['fullname']
            key.mobile_number = request.form['mobile_number']
            key.dob = request.form['date']
            key.interested_categories = request.form.getlist('category')
            x = request.form['userstatus']
            if x == 'True':
                key.users_status = True
            else:
                key.users_status = False
            key.put()
            sleep(1.00)
            return redirect(url_for('admin_home'))


@app.route('/admin-delete-user', methods=['POST'])
def admin_delete_user():
    if session['admin']:
        if request.method == 'POST':
            email = request.args.get('email')
            keys = Users.query(Users.email == email).fetch()
            for user in keys:
                user.key.delete()
            sleep(1.00)
            return redirect(url_for('admin_home'))


@app.route('/admin-edit-post', methods=['GET', 'POST'])
def admin_edit_post():
    if session['admin']:
        if request.method == 'POST':
            post_id = request.args.get('post_id')
            t = Posts.query().fetch()
            categories = Categories.query().fetch()
            posts = []
            for p in t:
                if int(p.key.id()) == int(post_id):
                    posts.append(p)
            print posts
            return render_template('admin-edit-post.html', posts=posts, categories=categories)


@app.route('/admin-update-post', methods=['GET', 'POST'])
def admin_update_post():
    if session['admin']:
        if request.method == 'POST':
            post_id = request.form['post_id']
            post_title = request.form['post_title']
            email = request.form['email']
            selected_category = request.form['category_selected']
            post_status = request.form['userstatus']
            list1 = request.form.getlist('list')
            posts = Posts.query().fetch()
            p = ""
            for post in posts:
                if post.key.id() == int(post_id):
                    p = post
            uploaded_file = request.files.get('file')
            print type(uploaded_file)
            p.post_title = post_title
            p.email = email
            p.category_name = selected_category
            p.post_list = list1
            categories = Categories.query(Categories.category_name == selected_category).fetch()
            if post_status == 'True':
                if categories[0].category_status == True:
                    p.post_status = True
            else:
                p.post_status = False
            p.put()
            sleep(1.00)
            return redirect(url_for('admin_home'))


@app.route('/admin-update-post-image', methods=['GET', 'POST'])
def admin_update_post_image():
    if session['admin']:
        if request.method == 'GET':
            post_id = request.args.get('post_id')
            return render_template('admin-update-post-image.html', post_id=post_id)
        else:
            post_id = request.args.get('post_id')
            print post_id
            uploaded_file = request.files.get('file')
            if request.files.get('file', None):
                print "Hahaha"
                print type(uploaded_file)
                alt = request.form.get('alt')
                mimetype = uploaded_file.mimetype
                image_data = uploaded_file.stream.read()
                blob = images.resize(image_data, 500, 500)
            else:
                print "Blah"
                alt = ""
                mimetype = ""
                image_data = ""
                blob = ""
            posts = Posts.query().fetch()
            p = ""
            for post in posts:
                if post.key.id() == int(post_id):
                    p = post
            p.alt = alt
            p.mimetype = mimetype
            p.image_data = image_data
            p.blob = blob
            p.put()
            return redirect(url_for('homepage'))


@app.route('/admin-delete-post', methods=['POST'])
def admin_delete_post():
    if session['admin']:
        if request.method == 'POST':
            post_id = request.args.get('post_id')
            keys = Posts.query().fetch()
            for post in keys:
                if post.key.id() == int(post_id):
                    post.key.delete()
            sleep(1.00)
            return redirect(url_for('admin_home'))


@app.route('/admin-edit-category', methods=['GET', 'POST'])
def admin_edit_category():
    if session['admin']:
        if request.method == 'POST':
            id = request.args.get('category_id')
            category = ndb.Key(urlsafe=id)
            categories = category.get()
            return render_template('admin-edit-category.html', categories=categories)


@app.route('/admin-update-category', methods=['GET', 'POST'])
def admin_update_category():
    if session['admin']:
        if request.method == 'POST':
            id = request.args.get('category_id')
            category_key = ndb.Key(urlsafe=id)
            category = category_key.get()
            category.category_name = request.form['category_name']
            status = request.form['category_status']
            if status == 'True':
                category.category_status = True
            else:
                category.category_status = False
                posts = Posts.query(Posts.category_name == category.category_name).fetch()
                for post in posts:
                    post.post_status = False
                    post.put()
            print category
            category.put()
            sleep(1.00)
            return redirect(url_for('admin_home'))


@app.route('/admin-delete-category', methods=['POST'])
def admin_delete_category():
    if session['admin']:
        if request.method == 'POST':
            id = request.args.get('category_id')
            category_key = ndb.Key(urlsafe=id)
            category = category_key.get()
            posts = Posts.query(Posts.category_name == category.category_name).fetch()
            for post in posts:
                post.key.delete()
            category.key.delete()
            sleep(1.00)
            return redirect(url_for('admin_home'))


@app.route('/autofill', methods=['GET', 'POST'])
def autofill():
    return render_template('autofill.html')


@app.route('/suggestions-json', methods=['POST'])
def suggestions_json():
    url = request.json['data']
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return jsonify(data)


@app.route('/search', methods=['POST'])
def search():
    print('in search post method')
    search_query = request.json['data']
    print(search_query)
    posts = Posts.query().fetch()
    search_list = []
    for post in posts:
        print(search_query)
        print(post.post_title.find(search_query))
        if post.post_title.lower().find(search_query.lower()) != -1 and search_query != '':
            search_list.append([post.post_title, post.email, post.key.id()])
    print(search_list)
    return jsonify(search_list)


@app.route('/search-tags', methods=['POST'])
def search_tags():
    print('in search tags method')
    # search_query = request.json['data']
    # print(search_query)
    posts = Posts.query().fetch()
    search_tag_list = {}
    for post in posts:
        for tag in post.post_tags:
            search_tag_list[tag] = None
        # print(search_query)
        # print(post.post_tags.find(search_query))
        # if post.post_tags.lower().find(search_query.lower()) != -1 and search_query != '':
        #     search_tag_list.append([post.post_tags, post.key.id()])
    print(search_tag_list)
    return jsonify(search_tag_list)


@app.route('/add-tags', methods=['POST'])
def add_tags():
    print('in add tags post method')
    data = request.json['tags']
    data = data.split('close')
    print(data)
    return jsonify(True)


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin-login.html')
    else:
        username = request.form['email']
        password = request.form['password']
        if username == app.config['USERNAME'] and password == app.config['PASSWORD']:
            session.pop('user', None)
            session['admin'] = 'admin'
            return redirect(url_for('admin_home'))
        else:
            return render_template('admin-login.html', error='Invalid Credentials')


@app.route('/admin-logout', methods=['GET'])
def admin_logout():
    if request.method == 'GET':
        session.pop('admin', None)
        return render_template('homepage.html')


@app.route('/login-social', methods=['GET'])
def login_social():
    return render_template('login_social.html')


@app.route('/fb-user-management', methods=['POST'])
def fb_user_management():
    full_name = request.json['name']
    print('name = ' + full_name)
    email = request.json['email']
    print('email = ' + email)
    users = Users.query().fetch()
    for user in users:
        if user.email == email:
            print('already unnadu vedu')
            session['user'] = email
            return jsonify('exists')
    print('vedu kotta odu')
    new_user = Users(email=email, full_name=full_name, user_type='facebook')
    new_user.put()
    session['user'] = email
    sleep(1.00)
    return jsonify('new_user')


@app.route('/auto-top10', methods=['GET'])
def auto_top10():
    print('in auto top 10')
    movies = Movies.query().order(-Movies.weight).fetch(10)
    print(movies)
    print(len(movies))
    return render_template('auto-top10.html', top10=movies)


@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'GET':
        categories = Categories.query(Categories.category_status == True).fetch()
        post_list = Posts.query(Posts.post_status == True).fetch()
        return render_template('categories.html', categories=categories, post_list=post_list)
    else:
        print("In Category Posts")
        categories = Categories.query(Categories.category_status == True).fetch()
        print(categories)
        category_list = []
        for category in categories:
            category_list.append(category.category_name)
        return jsonify(category_list)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    if request.method == 'GET':
        return render_template('statistics.html')


@app.route('/graph_results', methods=['POST'])
def graph_results():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    today = datetime.datetime.now()
    posts = Posts.query(
        ndb.AND(Posts.post_status == True, Posts.created_date < today, Posts.created_date > yesterday)).fetch()
    maxlikes = 0
    maxpost = []
    cat = {}
    tags = {}
    for post in posts:
        if len(post.liked_posts) > maxlikes:
            maxlikes = len(post.liked_posts)
            maxpost = post
        for tag in post.post_tags:
            if tag != '':
                if not tag in tags:
                    tags[tag] = 1
                else:
                    tags[tag] += 1
        if not post.category_name in cat:
            cat[post.category_name] = 1
        else:
            cat[post.category_name] += 1
    temp_dict = {'post_id': maxpost.key.id(), 'post_title': maxpost.post_title, 'email': maxpost.email,
                 'category_name': maxpost.category_name, 'post_list': maxpost.post_list,
                 'liked_posts': maxpost.liked_posts, 'created_date': maxpost.created_date}
    if len(tags) > 10:
        tags_dict = dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10])
    else:
        tags_dict = dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:len(tags)])
    return jsonify(cat, tags_dict, temp_dict)


if __name__ == '__main__':
    app.run(debug=True)
