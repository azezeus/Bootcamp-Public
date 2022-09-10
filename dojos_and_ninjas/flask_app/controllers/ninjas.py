from flask import render_template, redirect, request,session,flash
from flask_app import app
from flask_app.models import dojo, ninja

@app.route('/ninjas')
def ninjas():
    
    return render_template('ninja.html',dojos= dojo.Dojo.get_all())


@app.route('/create/ninja',methods=['POST'])
def create_ninja():
    ninja.Ninja.save(request.form)
    return redirect('/')

@app.route('/ninja/delete/<int:id>')
def delete(id):
    data ={
        "id": id
    }
    ninja.Ninja.delete(data)
    return redirect('/')

@app.route('/ninja/edit/<int:id>')
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit_ninja.html", ninja=ninja.Ninja.get_one(data))

@app.route('/ninja/update',methods=['POST'])
def update():
    ninja.update(request.form)
    return redirect('/')
    # tried using '/dojo/{{id}}' as my redirect path, but it would not work.