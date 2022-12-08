#!/usr/bin/python3
"""view of State object"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def get_all_cities(state_id):
    """return all cities objects"""
    state_list = []
    all_objs = storage.all(State)
    obj = storage.get("State", state_id)
    for obj in all_objs.values():
        state_list.append(obj.to_dict())
    if obj is None:
        abort(404)
    return jsonify(state_list)


@app_views.route('/states/<city_id>', methods=["GET"])
def get_city(city_id):
    """return json City object"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def city_delete(city_id):
    """delete an object by id"""
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"], strict_slashes=False)
def post_obj_city():
    """add new state object"""
    dic = {}
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    if "name" not in dic.keys():
        abort(400, "Missing name")
    new_state = City(**dic)
    for k, v in dic.items():
        setattr(new_state, k, v)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_obj_city(city_id):
    """update new state object"""
    dic = {}
    obj = storage.get("City", city_id)
    if obj is None:
        abort(404)
    dic = request.get_json(silent=True)
    if dic is None:
        abort(400, "Not a JSON")
    for key, value in dic.items():
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
