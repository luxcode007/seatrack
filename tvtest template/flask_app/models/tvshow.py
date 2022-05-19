from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Tvshow:
    db_name = 'tvshows_db'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.network = db_data['network']
        self.description = db_data['description']
        self.release_date = db_data['release_date']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO tvshows (title, network, description, release_date, user_id) VALUES (%(title)s,%(network)s,%(description)s,%(release_date)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tvshows;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_tvshows = []
        for row in results:
            print(row['release_date'])
            all_tvshows.append( cls(row) )
        return all_tvshows

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM tvshows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE tvshows SET title=%(title)s, network=%(network)s, description=%(description)s, release_date=%(release_date)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM tvshows WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_tvshow(tvshow):
        is_valid = True
        if len(tvshow['title']) < 3:
            is_valid = False
            flash("Title: must be at least 3 characters","tvshow")
        if len(tvshow['network']) < 3:
            is_valid = False
            flash("Network: must be at least 3 characters","tvshow")
        if tvshow['release_date'] == "":
            is_valid = False
            flash("Release Date: Please enter a release date","tvshow")
        if len(tvshow['description']) < 3:
            is_valid = False
            flash("Description: must be at least 3 characters","tvshow")
        return is_valid
