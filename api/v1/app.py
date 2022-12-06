#!/usr/bin/python3
"""start your API!"""


from flask import Flask
from flask import make_response
from flask import jsonify
from models import storage
from api.v1.views import app_views
from os import getenv as get


# create a variable app, instance of Flask
app = Flask(__name__)

# register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """
    declare a method to handle @app.teardown_appcontext that calls
    storage.close()
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    dict_error = {"error": "Not found"}
    return make_response(jsonify(dict_error), 404)


if __name__ == "__main__":
    host = get("HBNB_API_HOST", "0.0.0.0")
    port = get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True, debug=True)
