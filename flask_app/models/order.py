from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash 


class Order:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.boxes = data['boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def all_orders(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('cookies').query_db(query)
        orders = []

        for order in results:
            orders.append(cls(order))

        return orders

    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO orders (name, cookie_type, boxes, created_at, updated_at)
                VALUES (%(name)s, %(cookie_type)s, %(boxes)s, NOW(), NOW());
                """
        
        return connectToMySQL('cookies').query_db(query, data)

    @classmethod
    def one_order(cls, data):
        query = """
                SELECT * FROM orders 
                WHERE orders.id = %(id)s;
                """
        one_order = connectToMySQL('cookies').query_db(query,data)

        return cls(one_order[0])


    @classmethod
    def update(cls,data):
        query = """
                UPDATE orders 
                SET name =%(name)s, cookie_type =%(cookie_type)s, boxes=%(boxes)s, updated_at=NOW()
                WHERE id =%(id)s;
                """

        return connectToMySQL('cookies').query_db(query,data)




    @staticmethod
    def validate_order(data):
        is_valid = True 

        if not data['name']:
            flash("Name is required", "error")
            is_valid = False 
        
        elif len(data['name']) < 2:
            flash("Name must be at least 2 characters long.", "error")
            is_valid = False

        if not data['cookie_type']:
            flash("Cookie type is required")
            is_valid = False

        elif len(data['cookie_type']) < 2:
            flash("Cookie type must be at least 2 characters long.", "error")
            is_valid = False 

        if not data['boxes']:
            flash("Number of boxes is required")
            is_valid = False

        elif int(data['boxes']) < 0:
            flash("Enter valid number of boxes")
            is_valid = False

        return is_valid