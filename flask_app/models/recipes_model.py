from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import users_model
from flask import session, flash, redirect

db = "recipe_share"
class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.proteins_id = data['proteins_id']
        self.fiber= data['fiber']
        self.time = data['time']
        self.cuisine = data['cuisine']
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.users_id = data['users_id']
        self.chef = None
        self.protein = None

    @classmethod
    def save_recipe(cls,data):
        query = '''INSERT INTO recipes (recipe_name,time,cuisine,users_id,proteins_id,fiber) 
        VALUES (%(recipe_name)s,%(time)s,%(cuisine)s,%(users_id)s,%(proteins_id)s,%(fiber)s);'''
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def update_recipe(cls,data):
        query = '''UPDATE recipes SET recipe_name=%(recipe_name)s,
        proteins_id=%(proteins_id)s,fiber=%(fiber)s,
        time=%(time)s,cuisine=%(cuisine)s
        WHERE recipes.id =%(id)s;'''
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        return result

    @classmethod
    def get_one(cls,data):
        query  = '''SELECT * FROM recipes 
        JOIN users ON recipes.users_id = users.id
        JOIN proteins ON recipes.proteins_id = proteins.id
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
        protein_data = {
            'id' : ['proteins.id'],
            'protein_name' : ['protein_name'],
            'calories' : ['calories'],
            'macros' : ['macros'],
            'diet' : ['diet']
            }
        recipe.chef = users_model.User(user_data)
        recipe.protein = Protein(protein_data)
        return recipe

    @classmethod
    def get_ingredient(cls,data):
        query  = '''SELECT * FROM recipes 
        JOIN users ON recipes.users_id = users.id
        JOIN proteins ON recipes.proteins_id = proteins.id
        WHERE proteins_id = %(id)s;'''
        results = connectToMySQL(db).query_db(query,data)
        collection = []
        print(results,"___________------------_____________")
        for row in results:
            recipe = cls(row)
            print(collection,"---------------------------------")
            chef_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'color_icon' : row['color_icon'],
                'password' : row['password']
                }
            protein_data = {
                'id' : row['proteins.id'],
                'protein_name' : row['protein_name'],
                'calories' : row['calories'],
                'macros' : row['macros'],
                'diet' : row['diet']
                }
            recipe.chef = users_model.User(chef_data)
            recipe.protein = Protein(protein_data)
            collection.append(recipe)
        return collection

    @classmethod
    def save_ingredient(cls,data):
        query = '''INSERT INTO proteins (protein_name,calories,macros,diet,updated_at)   
        VALUES (%(protein_name)s,%(calories)s,%(macros)s,%(diet)s,NOW());'''
        result = connectToMySQL(db).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        if 'user_id' not in session:
            return redirect('/')
        query = '''SELECT * FROM recipes 
        JOIN users ON recipes.users_id = users.id
        JOIN proteins ON recipes.proteins_id = proteins.id;'''
        result = connectToMySQL(db).query_db(query)
        collection = []
        for row in result:
            recipe = cls(row)
            chef_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'color_icon' : row['color_icon'],
                'password' : row['password']
                }
            protein_data = {
                'id' : row['proteins.id'],
                'protein_name' : row['protein_name'],
                'calories' : row['calories'],
                'macros' : row['macros'],
                'diet' : row['diet']
                }
            recipe.chef = users_model.User(chef_data)
            recipe.protein = Protein(protein_data)
            collection.append(recipe)
        return collection

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
        if len(recipe['cuisine']) < 3:
            flash("Type of Cuisine must be at least 3 characters.")
            is_valid = False
        if recipe['time'] =="":
            flash("Time must be entered.")
            is_valid = False    
        return is_valid

    @staticmethod
    def validate_ingredient(ingredient):
        is_valid = True
        if len(ingredient['protein_name']) < 2:
            flash("Recipe name must be at least 2 characters.")
            is_valid = False
        if ingredient['calories'] is not int:
            flash("Calories must be entered in an integer format.")
            is_valid = False
        if ingredient['macros'] is not int:
            flash("Macros must be entered in an integer format.")
            is_valid = False    
        return is_valid

    

class Protein:
    def __init__(self,data):
        self.id = data.get('id')
        self.protein_name = data.get('protein_name')
        self.calories = data.get('calories')
        self.macros = data.get('macros')
        self.diet = data.get('diet')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    @classmethod
    def get_all(cls):
        if 'user_id' not in session:
            return redirect('/')
        query = '''SELECT * FROM proteins'''
        results = connectToMySQL(db).query_db(query)
        collection = []
        print(results)
        for row in results:
            print(row)
            protein = cls(row)
            collection.append(protein)
        return collection

    @classmethod
    def get_one(cls,data):
        query  = '''SELECT * FROM proteins 
        WHERE proteins.id = %(id)s;'''
        result = connectToMySQL(db).query_db(query,data)
        recipe = cls(result[0])
        user_data ={
            'id' : result[0]['users.id'],
            'first_name' : result[0]['first_name'],
            'last_name' : result[0]['last_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password']
        }
        recipe.chef = users_model.User(user_data)
        return recipe