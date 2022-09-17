
from flask import render_template,redirect,request,session,flash
from flask_app import app
app.secret_key = "shhhhhh"
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/register', methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')

@app.route('/login', methods=['post'])
def login():
    user = User.check_email(request.form)
    if user == False:
        flash("Login credentials were not sufficient")
        return redirect("/")
    else:
        if bcrypt.check_password_hash(user.password, request.form['password']) == True:
            session['user_id'] = user.id
            session['email'] = user.email
            session['first_name'] = user.first_name
            return redirect('/dashboard')
        else:
            flash("Login credentials were not sufficient")
            return redirect("/")

@app.route('/dashboard')
def success():
    data = {
        "id": session['user_id']
    }
    return render_template("posted_recipes.html", recipes=Recipe.get_all(), user=User.get_by_id(data))

@app.route("/recipe/new", methods=['get'])
def new():
    data = {
        "id": session['user_id']
    }
    return render_template('create.html', user=User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
