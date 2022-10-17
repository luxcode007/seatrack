from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

# seatrack_db is the DATABASE UPDATE ALL FILES

db="seatrack_db"

# notes on connecting the many to many data
# watchlists = db.Table('watchlists',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('collection_id', db.Integer, db.ForeignKey('channel.id'))

# )

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # for many to many relationship
        self.collections = []
    db = "seatrack_db"

# class User(db.Model):
#     following = db.relationship('Collection', secondary=watchlists)

#     def __repr__(self):
#         return f'<User: {self.data}>'

    @classmethod
    def get_user_collections( cls , data ):
        query = "SELECT * FROM users LEFT JOIN watchlists ON watchlists.user_id = user.id LEFT JOIN collections ON watchlists.collection_id = collection.id WHERE user.id = %(id)s;"
        results = connectToMySQL('users').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row.
        user = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            collection_data = {
                "id" : row_from_db["collection.id"]
                # "name" : row_from_db["name"],
                # "slug" : row_from_db["slug"],
                # "notes" : row_from_db["notes"],
                # "created_at" : row_from_db["collections.created_at"],
                # "updated_at" : row_from_db["collections.updated_at"]
            }
            # from flask_app.models import collection to prevent circular imports
            from flask_app.models import collection
            user.collections.append( collection.Collection( collection_data ) )
        return user

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid

# staticmethod for login validation using database & bcrypt hashing for password
    # @staticmethod
    # def validate_login(user):
    #     is_valid = True
    #     query = "SELECT * FROM users WHERE email = %(email)s;"
    #     results = connectToMySQL(User.db).query_db(query,user)
    #     if (results) >= 1:
    #         flash("Email already taken.","register")
    #         is_valid=False
        # if not EMAIL_REGEX.match(user['email']):
        #     flash("Invalid Email!!!","register")
        #     is_valid=False
        # if len(user['first_name']) < 3:
        #     flash("First name must be at least 3 characters","register")
        #     is_valid= False
        # if len(user['last_name']) < 3:
        #     flash("Last name must be at least 3 characters","register")
        #     is_valid= False
        # if len(user['password']) < 8:
        #     flash("Password must be at least 8 characters","register")
        #     is_valid= False
        # if user['password'] != user['confirm']:
        #     flash("Passwords don't match","register")
        # return is_valid