#!/usr/bin/python3
"""view of amenity object"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"],  strict_slashes=False)
def amenity_ret():
    """return json amenity objects"""
    ame_list = []
    all_objs = storage.all(Amenity)
    for obj in all_objs.values():
        ame_list.append(obj.to_dict())
    return jsonify(ame_list)


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
def amenity_get_by_id(amenity_id):
    """return json amenity objects by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def amenity_delete(amenity_id=None):
    """delete an object by id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=["POST"], strict_slashes=False)
def post_amenity_obj():
    """add new amenity object"""
    dic = {}
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "name" not in dic.keys():
        abort(400, "Missing name")
    new_ame = Amenity.Amenity()
    for k, v in dic.items():
        setattr(new_ame, k, v)
    storage.new(new_ame)
    storage.save()
    return jsonify(new_ame.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"])
def update_amenity_obj(amenity_id=None):
    """update new amenity object"""
    dic = {}
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
