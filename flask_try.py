from path_finder import PathFinder
from structures import Coords
from flask import Flask, jsonify, request
#from json import jsonify
app = Flask(__name__)


pf = PathFinder()

@app.route('/', methods=['POST'])
def execute_smartshopping():
    content = request.get_json(silent=True)
    print(content)
    activities = []
    for activity in content['activities']:
        activities.append(activity)

    home_coords = Coords(latitude=content['latitude'], longitude=content['longitude'])
    best_path = pf.find_best_path(desired_activities=activities, my_coords=home_coords)
    print(best_path)
    return jsonify(best_path)