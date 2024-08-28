from flask import Blueprint, request, jsonify
from model.location import db, Location


location_bp = Blueprint('location', __name__, url_prefix='/api/locations')


@location_bp.route("/", methods=["GET"])
def get_locations():
    locations = Location.query.all()

    print("Successfully fetched all locations")
    locations_list = [{'id': location.id, 'name': location.name} for location in locations]

    return jsonify(locations_list), 200
     
@location_bp.route("/", methods=["POST"])
def create_location():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'error': 'The name field is required.'}), 400

    existing_location = Location.query.filter_by(name=data['name']).first()
    if existing_location is not None:
        return jsonify({'error': 'Location with this name already exists.'}), 400
    
    new_location = Location(name=data['name'])
    print(f"Creating new location {new_location.name}")

    db.session.add(new_location)
    db.session.commit()

    return jsonify({'id': new_location.id, 'name': new_location.name}), 201

