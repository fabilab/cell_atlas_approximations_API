"""
Web application supporting the cell atlas approximation API
"""
from flask import (
    Flask,
)
from flask_restful import Api
from config import configuration as config
from api import (
    get_api_endpoint,
    api_dict,
)


##############################
app = Flask(__name__, static_url_path="/static", template_folder="templates")
app_api = Api(app)
with open('secret_key.txt') as f:
    app.config['SECRET_KEY'] = f.read()
##############################


# Connect to endpoints
for api_name, api_object in api_dict.items():
    app_api.add_resource(api_object, get_api_endpoint(api_name))


# Main loop
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
