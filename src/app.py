"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# initial members of the family
jackson_family.add_member({"id": jackson_family._generateId(),
                            "first_name": "John",
                            "last_name": jackson_family.last_name,
                            "age": 33,
                            "lucky_numbers": [7, 13, 22]})

jackson_family.add_member({"id": jackson_family._generateId(),
                            "first_name": "Jane",
                            "last_name": jackson_family.last_name,
                            "age": 35,
                            "lucky_numbers": [10, 14, 3]})

jackson_family.add_member({"id": jackson_family._generateId(),
                            "first_name": "Jimmy",
                            "last_name": jackson_family.last_name,
                            "age": 5,
                            "lucky_numbers": [1]})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get All Family Members
@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()


    return jsonify(members), 200

# Create Member
@app.route('/member', methods=['POST'])
def create_member():
    if request.method == 'POST':
        new_member = request.json
        for i in ["first_name", "age", "lucky_numbers", "id"]:
            if i not in new_member:
                return "You must provide all properties to create a family member.", 400

        new_member["last_name"] = jackson_family.last_name     
        jackson_family.add_member(new_member)
        return "New family member added.", 200

# Get Member
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id=None):
    if request.method == 'GET':
        member = jackson_family.get_member(id)
        if member:
            return member, 200
        else:
            return "Family member not found.", 404

# Delete Member
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id=None):
    if request.method == 'DELETE':
        member = jackson_family.delete_member(id)
        if member:
            return {"done": True}, 200
        else:
            return "Family member not found.", 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
