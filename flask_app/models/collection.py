from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Collection:
    db_name = 'seatrack_db'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.slug = db_data['slug']
        self.notes = db_data['notes']
        # self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        # for many to many relationship
        self.users = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO collections (name, slug, notes) VALUES (%(name)s,%(slug)s,%(notes)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_collection_users( cls , data ):
        query = "SELECT * FROM collections LEFT JOIN watchlists ON watchlists.collection_id = collection.id LEFT JOIN users ON watchlists.user_id = user.id WHERE collections.id = %(id)s;"
        results = connectToMySQL('users').query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row.
        collection = cls( results[0] )
        for row_from_db in results:
            # Now we parse the topping data to make instances of toppings and add them into our list.
            user_data = {
                "id" : row_from_db["user.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "created_at" : row_from_db["collections.created_at"],
                "updated_at" : row_from_db["collections.updated_at"]
            }
        # from flask_app.models import user
        from flask_app.models import user
        collection.users.append(user.User(user_data ) )
        return collection

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM collections;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_collections = []
        for row in results:
            print(row['created_at'])
            all_collections.append( cls(row) )
        return all_collections

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM collections WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE collections SET name=%(name)s, slug=%(slug)s, notes=%(notes)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM collections WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_collection(collection):
        is_valid = True
        if len(collection['name']) < 3:
            is_valid = False
            flash("the name must be at least 3 characters","collection")
        if len(collection['slug']) < 2:
            is_valid = False
            flash("the slug must be at least 2 characters","collection")
        if len(collection['notes']) < 3:
            is_valid = False
            flash("The notes must be at least 3 characters","collection")
        # if collection['date_made'] == "":
        #     is_valid = False
        #     flash("Please enter a date","collection")
        return is_valid

