"""
Web application supporting the cell atlas approximation API
"""
from flask import (
    Flask,
)
from flask_restful import Api
from config import configuration as config
from api.endpoints import get_api_endpoint
from api.objects import (
    Average,
    Celltypes,
    Features,
    FractionDetected,
    Markers,
    Organisms,
    Organs,
)


##############################
app = Flask(__name__, static_url_path="/static", template_folder="templates")
app_api = Api(app)
with open('secret_key.txt') as f:
    app.config['SECRET_KEY'] = f.read()
##############################


# Connect to endpoints
app_api.add_resource(Organisms, get_api_endpoint('organisms'))
app_api.add_resource(Organs, get_api_endpoint('organs'))
app_api.add_resource(Features, get_api_endpoint('features'))
app_api.add_resource(Celltypes, get_api_endpoint('celltypes'))
app_api.add_resource(Average, get_api_endpoint('average'))
app_api.add_resource(FractionDetected, get_api_endpoint('fraction_detected'))
app_api.add_resource(Markers, get_api_endpoint('markers'))


# Main loop
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
