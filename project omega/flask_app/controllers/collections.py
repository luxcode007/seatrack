from flask import render_template, session,flash,redirect, request
import requests
# need import requests for get function call
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.collection import Collection

@app.route('/new/collection')
def new_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('create.html',user=User.get_by_id(data))


@app.route('/create/collection',methods=['POST'])
def create_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Collection.validate_collection(request.form):
        return redirect('/new/collection')
    data = {
        "name": request.form["name"],
        "slug": request.form["slug"],
        "notes": request.form["notes"],
        "user_id": session["user_id"]
    }
    collection_id = Collection.save(data)
    watchlist_data = {
        "user_id": session["user_id"],
        "collection_id": collection_id
    }
    Collection.save_watchlist(watchlist_data)
    return redirect('/dashboard')

@app.route('/edit/collection/<int:id>')
def edit_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",edit=Collection.get_one(data),user=User.get_by_id(user_data))

# see /collection/ below for original
# @app.route('/view/collection/<int:id>/')
# def edit_collection(id, slug):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id":id
#     }
#     user_data = {
#         "id":session['user_id']
#     }
#     # request.get api call f(link x/{slug.slug}/stats
#     slug = Collection.get_one(data)
#     # slug is needed for api
#     # apiData = request.get api call flink x/{slug.slug}/stats
#     return render_template("view.html",edit=Collection.get_one(data),user=User.get_by_id(user_data), apiData=apiData)

@app.route('/update/collection',methods=['POST'])
def update_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Collection.validate_collection(request.form):
        return redirect('/new/collection')
    data = {
        "name": request.form["name"],
        "slug": request.form["slug"],
        "notes": request.form["notes"],
        "id": request.form['id']
    }
    Collection.update(data)
    return redirect('/dashboard')

@app.route('/collection/<int:id>')
def show_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    # favorites = Collection.get_favorites(data)
    # add code to call on watchlist to connect the collection to len() users who favorited
    # define the collection class again in this route to pull slug from the Collection.get_one() method defined in models for the class.
    collection = Collection.get_one(data)
    slug = collection.slug
    url = f"https://api.opensea.io/api/v1/collection/{slug}"
    headers = {"Accept": "application/json", "X-API-KEY": "f33a8411e29b4f69b1a1c5e431e9e43d"}
    response = requests.get(url, headers=headers)
    # print(response.json())
    # slug is needed for api
    # apiData = request.get api call flink x/{slug.slug}/stats
    return render_template("collection.html",collection=Collection.get_one(data),user=User.get_by_id(user_data), apiData=response.json())

@app.route('/addwatchlist/<int:id>')
def save_watchlist(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "collection_id":id,
        "user_id":session['user_id']
    }
    Collection.save_watchlist(data)
    return redirect(f'/collection/{id}')

@app.route('/destroy/collection/<int:id>')
def destroy_collection(id):
    # if 'user_id' not in session:
    #     return redirect('/logout')
    data = {
        "id":id
    }
    Collection.destroy(data)
    return redirect('/dashboard')

# @app.route('/get_data/<int:id>', methods=['POST'])
# def get_data():
#     slug = request.form['slug']
#     url = f"https://api.opensea.io/api/v1/collection/{slug}/stats"
#     response = requests.get(url)
#     print(response.json())
#     return redirect('/collection/<int:id>',collection=Collection.get_one(data))