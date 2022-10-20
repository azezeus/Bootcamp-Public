from flask import render_template,redirect,request,session,flash
from flask_app import app
app.secret_key = "shhhhhh"
from flask_app.models.recipes_model import Recipe, Protein
from flask_app.models.users_model import User


@app.route('/create', methods=['POST','GET'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe (request.form):
        return redirect('/recipe/new')
    data = {
        "recipe_name" : request.form['recipe_name'],
        "proteins_id": request.form['proteins_id'],
        "fiber": request.form['fiber'],
        "time" : request.form['time'],
        "cuisine" : request.form['cuisine'],
        "users_id": session['user_id']
    }
    Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route("/recipe/new", methods=['GET'])
def new():
    data = {
        "id": session['user_id']
    }
    return render_template('createRecipe.html', user=User.get_by_id(data), proteins=Protein.get_all())

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        "id": id
    }
    return render_template("editRecipe.html", recipe=Recipe.get_one(data), proteins=Protein.get_all())


@app.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit/<int:id>')
    data = {
        'id' : request.form['id'],
        'recipe_name' : request.form['recipe_name'],
        'proteins_id': request.form['proteins_id'],
        'fiber': request.form['fiber'],
        'time' : request.form['time'],
        'cuisine' : request.form['cuisine']
    }
    print(request.form['id'],"------------------------------------------")
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/selectProtein')
def selectProtein():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    return render_template('selectProtein.html', user=User.get_by_id(data), proteins=Protein.get_all())    

@app.route('/recipes/<int:id>', methods=['GET'])
def find(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    # create data dictionary for recipes & add another route (Lists all protein options, .get_all(protein)) & add a link on the proteins that lead to a new HTML with recipes
    return render_template("findRecipe.html", recipes=Recipe.get_ingredient(data))

@app.route('/addIngredients', methods=['POST','GET'])
def add_ingredient():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'protein_name': request.form['protein_name'],
        'calories': request.form['calories'],
        'macros' : request.form['macros'],
        'diet' : request.form['diet'],
    }
    Recipe.save_ingredient(data)
    return redirect('/dashboard')

@app.route("/ingredient/new", methods=['get'])
def add():
    data = {
        "id": session['user_id']
    }
    return render_template('addIngredient.html', user=User.get_by_id(data))

@app.route('/recipe/delete/<int:id>')
def delete(id):
    data ={
        "id": id
    }
    Recipe.delete(data)
    return redirect('/dashboard')