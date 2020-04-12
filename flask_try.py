from path_finder import PathFinder
from structures import Coords
from flask import Flask, jsonify
#from json import jsonify
app = Flask(__name__)

tipus = input("Donam un tipus de comperç: ")
tipus2 = input("Dona'm un tipus de comerç: ")
activities=[tipus, tipus2]
home_coords=Coords(x_utm=430226.85, y_utm=4581590.93)
pf = PathFinder()

@app.route('/')
def execute_smartshopping():
    return jsonify(pf.find_best_path(desired_activities=activities, my_coords=home_coords))