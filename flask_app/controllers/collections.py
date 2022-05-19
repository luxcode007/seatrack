from flask import render_template, session,flash,redirect, request
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
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": int(request.form["under30"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Collection.save(data)
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

@app.route('/update/collection',methods=['POST'])
def update_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Collection.validate_collection(request.form):
        return redirect('/new/collection')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under30": int(request.form["under30"]),
        "date_made": request.form["date_made"],
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
    return render_template("collection.html",collection=Collection.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/collection/<int:id>')
def destroy_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Collection.destroy(data)
    return redirect('/dashboard')
