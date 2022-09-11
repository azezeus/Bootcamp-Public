from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

class Order:
    def __init__(self,data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.number_of_boxes = data['number_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(profile):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('cookie_orders').query_db(query)
        orders = []
        for i in results:
            orders.append( profile(i) )
        return orders

    @classmethod
    def save(cls, data):
        query = "INSERT INTO orders (customer_name, cookie_type, number_of_boxes) VALUES (%(customer_name)s,%(cookie_type)s,%(number_of_boxes)s);"
        result = connectToMySQL('cookie_orders').query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM orders WHERE id = %(id)s";
        result = connectToMySQL('cookie_orders').query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE orders SET customer_name=%(customer_name)s,cookie_type=%(cookie_type)s,number_of_boxes=%(number_of_boxes)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('cookie_orders').query_db(query,data)

    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order['customer_name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(order['cookie_type']) < 2:
            flash("Cookie Type must be at least 2 characters.")
            is_valid = False
        if int(order['number_of_boxes']) < 0:
            flash("Quantity cannot be negative")
            is_valid = False
        return is_valid