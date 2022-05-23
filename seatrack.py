from flask_app import app
from flask_app.controllers import users, collections

# app = Flask(__name__) [this is in the __init__.py file]

if __name__ == "__main__":
    app.run(debug=True)