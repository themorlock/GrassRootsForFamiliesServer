import flask
from flask_restful import Resource, Api, reqparse
from flask import request
from flask import request, jsonify
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

FILE_NAME = '/Users/saakethvangati/Downloads/TXAustin19xx.geojson.txt'
json_file = json.load(open(FILE_NAME))


redlinings = []
for i in range(len(json_file['features'])):
	polygon_data = []
	for j in range(len(json_file['features'][i]['geometry']['coordinates'][0][0])):
		longitude, latitude = json_file['features'][i]['geometry']['coordinates'][0][0][j]
		polygon_data.append((longitude, latitude))
	redlinings.append((polygon_data, json_file['features'][i]['properties']['name'], json_file['features'][i]['properties']['area_description_data']))

def in_polygon(longitude, latitude, polygon_data):
	point = Point(longitude, latitude)
	polygon = Polygon(polygon_data)
	return polygon.contains(point)

@app.route('/get_redlining', methods=['GET'])
def get_redlining():
	parser = request.args
	coords = parser['coords'].split(',')
	longitude = float(coords[0])
	latitude = float(coords[1])
	for i in range(len(redlinings)):
		if in_polygon(longitude, latitude, redlinings[i][0]):
			return jsonify({'coordinates': redlinings[i][0], 'name': redlinings[i][1], 'area_description_data': redlinings[i][2]})
	return jsonify(['NULL'])

app.run()
