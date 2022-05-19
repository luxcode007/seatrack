from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tvshow import Tvshow

@app.route('/new/tvshow')
def new_tvshow():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('create.html',user=User.get_by_id(data))


@app.route('/add/show',methods=['POST'])
def add_tvshow():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tvshow.validate_tvshow(request.form):
        return redirect('/new/tvshow')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Tvshow.save(data)
    return redirect('/dashboard')

@app.route('/edit/tvshow/<int:id>')
def edit_tvshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",edit=Tvshow.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/tvshow',methods=['POST'])
def update_tvshow():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tvshow.validate_tvshow(request.form):
        return redirect('/new/tvshow')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "id": request.form['id']
    }
    Tvshow.update(data)
    return redirect('/dashboard')

@app.route('/tvshow/<int:id>')
def show_tvshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("tvshow.html",tvshow=Tvshow.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/tvshow/<int:id>')
def destroy_tvshow(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Tvshow.destroy(data)
    return redirect('/dashboard')
