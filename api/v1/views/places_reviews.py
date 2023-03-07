#!/usr/bin/python3
""" Module API for Places Review"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


# Retrieves the list of all Review objects of a Place:
@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id=None):
    """ List all Reviews """
    n_place = storage.get(Place, place_id)
    if n_place is None:
        abort(404)
    n_reviews = [review.to_dict() for review in n_place.reviews]
    return jsonify(n_reviews)


# Retrieves a Review object. : GET /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>/', methods=['GET'],
                 strict_slashes=False)
def show_one_review(review_id):
    """ show review """
    n_review = storage.get(Review, review_id)
    if n_review is None:
        abort(404)
    return jsonify(n_review.to_dict())


# Deletes a Review object: DELETE /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete Review """
    n_review = storage.get(Review, review_id)
    if n_review is None:
        abort(404)
    storage.delete(n_review)
    storage.save()
    return jsonify({}), 200


# Creates a Review: POST /api/v1/places/<place_id>/reviews
@app_views.route('/places/<place_id>/reviews/', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create New Review """
    opc_reqst = request.get_json()
    if opc_reqst is None:
        return 'Not a JSON', 400
    if 'user_id' not in opc_reqst.keys():
        return 'Missing user_id', 400
    if 'text' not in opc_reqst.keys():
        return 'Missing text', 400
    n_place = storage.get(Place, place_id)
    if n_place is None:
        abort(404)
    n_user = storage.get(User, opc_reqst['user_id'])
    if n_user is None:
        abort(404)
    reviews = Review(**opc_reqst)
    reviews.place_id = place_id
    reviews.save()
    return jsonify(reviews.to_dict()), 201


# Updates a Review object: PUT /api/v1/reviews/<review_id>
@app_views.route('/reviews/<review_id>/', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Update Review """
    n_review = storage.get(Review, review_id)
    if n_review is None:
        abort(404)
    opc_reqst = request.get_json()
    if opc_reqst is None:
        return 'Not a JSON', 400
    for key in ('id', 'user_id', 'place_id', 'created_at', 'update_at'):
        opc_reqst.pop(key, None)
    for key, value in opc_reqst.items():
        setattr(n_review, key, value)
    n_review.save()
    return jsonify(n_review.to_dict()), 200
