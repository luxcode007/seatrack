from flask import render_template,redirect,request,session,flash
import requests
# need requests for get function call
from flask_app import app
from flask_app.models.user import User
from flask_app.models.collection import Collection
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("landing.html")

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

# original old dashboard route before API connection to dashboard (see below)
# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         'id': session['user_id']
#     }
#     return render_template("dashboard.html",user=User.get_by_id(data),collections=Collection.get_all())

# Shout out to David S!!!!!!! Thank you!
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    collections = Collection.get_all()
    apiData = []
    for collection in collections:
        slug = collection.slug
        url = f"https://api.opensea.io/api/v1/collection/{slug}"
        headers = {"Accept": "application/json", "X-API-KEY": "f33a8411e29b4f69b1a1c5e431e9e43d"}
        response = requests.get(url, headers=headers)
        # print(response.json())
        collection.data=response.json()
        apiData.append(collection)
    return render_template("dashboard.html",user=User.get_by_id(data),collections=apiData)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')