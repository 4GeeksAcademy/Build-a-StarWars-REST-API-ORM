"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people(): 
    people = User.query.all()
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize()), 200
    else:
        raise APIException("Person not found", status_code=404)

@app.route('/planets', methods=['GET'])
def get_planets():
    pass

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    pass

@app.route('/users', methods=['GET'])
def get_users():
    pass

@app.route('/users/favorites', methods=['GET'])
def get_user_fav():
    pass

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_fav(planet_id):
    pass


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_fav(people_id):
    pass

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    pass

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    pass

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
