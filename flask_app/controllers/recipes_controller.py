from flask import render_template,redirect,request,session,flash
from flask_app import app
app.secret_key = "shhhhhh"
from flask_app.models.recipes_model import Recipe



@app.route('/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    data = {
        'recipe_name' : request.form['recipe_name'],
        'description' : request.form['description'],
        'under_thirty': request.form['under_thirty'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'users_id': session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit.html", recipe=Recipe.get_one(data))

@app.route('/show/<int:id>')
def show(id):
    data ={
        "id":id
    }
    return render_template("recipe.html", recipe=Recipe.get_one(data))

@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit/<int:id>')
    data = {
        'recipe_name' : request.form['recipe_name'],
        'description' : request.form['description'],
        'under_thirty': request.form['under_thirty'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'users_id': session['user_id']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/recipe/delete/<int:id>')
def delete(id):
    data ={
        "id": id
    }
    Recipe.delete(data)
    return redirect('/dashboard')