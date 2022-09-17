from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import users_model
from flask import session, flash, redirect

db = "recipes"
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty= data['under_thirty']
        self.date_made= data['date_made']
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.users_id = data['users_id']
        self.baker = None

    @classmethod
    def save_recipe(cls,data):
        query = "INSERT INTO recipes (recipe_name,description,instructions,under_thirty,date_made,users_id) VALUES (%(recipe_name)s, %(description)s, %(instructions)s,%(under_thirty)s, %(date_made)s, %(users_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET recipe_name=%(recipe_name)s,description=%(description)s,instructions=%(instructions)s,under_thirty=%(under_thirty)s,date_made=%(date_made)s,users_id=%(users_id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_one(cls,data):
        query  = '''SELECT * FROM recipes
        LEFT JOIN users ON recipes.users_id = users.id
        WHERE recipes.id = %(id)s;'''
        result = connectToMySQL(db).query_db(query,data)
        recipe = cls(result[0])
        user_data ={
            'id' : result[0]['users.id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password']
        }
        recipe.baker = users_model.User(user_data)
        return recipe

    @classmethod
    def get_all(cls):
        if 'user_id' not in session:
            return redirect('/')
        query = '''SELECT * from recipes 
        JOIN users on recipes.users_id = users.id;'''
        results = connectToMySQL(db).query_db(query)
        recipe_book = []
        print(results)
        for row in results:
            print(row)
            recipe = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password']
                }
            recipe.baker = users_model.User(user_data)
            recipe_book.append(recipe)
        return recipe_book

    @classmethod
    def delete(cls,data):
        query  = "DELETE from recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['recipe_name']) < 3:
            flash("Recipe name must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        if recipe['date_made'] =="":
            flash("Date made must be entered.")
            is_valid = False    
        return is_valid