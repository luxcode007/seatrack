from flask_app import app
from flask_app.controllers import users, recipes

# app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)