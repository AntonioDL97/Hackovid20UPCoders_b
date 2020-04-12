from path_finder import PathFinder
from structures import Coords
from flask import Flask, jsonify, request
#from json import jsonify
app = Flask(__name__)

content = request.get_json()
activities = []
for activity in content['activities']:
    activities.append(activity)

home_coords=Coords(latitude=content['latitude'], longitude=content['longitude'])
pf = PathFinder()

@app.route('/')
def execute_smartshopping():
    return jsonify(pf.find_best_path(desired_activities=activities, my_coords=home_coords))