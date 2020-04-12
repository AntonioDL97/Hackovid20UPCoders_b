from path_finder import PathFinder
from structures import Coords
from flask import Flask, jsonify
#from json import jsonify
app = Flask(__name__)

activities=['Fruiteries i verduleries', 'Carnisseries']
home_coords=Coords(x_utm=430226.85, y_utm=4581590.93)
pf = PathFinder()

@app.route('/')
def execute_smartshopping():
    return jsonify(pf.find_best_path(desired_activities=activities, my_coords=home_coords))