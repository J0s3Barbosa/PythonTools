# coding=utf-8
import base64
from app.image import ImagesDAO
from flask import Flask, jsonify, request, abort,Blueprint
import pymongo
from flask.templating import render_template
from app.config.app_config import mongo_config

imagesModule = Blueprint('images', __name__,
                        template_folder='templates')
try:
    client = pymongo.MongoClient(
        mongo_config['connectionString']
    )  
    database = client.images
    images_dao = ImagesDAO(database) 
except Exception as exc:
    print(exc)
    
class Monitor():

    @imagesModule.route('/monitor')
    def monitor():
        return render_template('monitoring.html')

    @imagesModule.route('/monitorhc')
    def monitorhc():
        return 'monitor module is Working!'

    @imagesModule.route('/images')
    def list():
        return jsonify(images_dao.list()), 200


    @imagesModule.route('/images/<pk>', methods=['GET', 'PUT'])
    def get(pk):
        if request.method == 'GET':
            return jsonify(images_dao.read(pk))


    @imagesModule.route('/images', methods=['POST'])
    def create():
        if request.method == 'POST':
            data = request.json
            title = data.get('title', None)
            description = data.get('description', None)

            if not title or not description:
                return "The fields 'title' and 'description' are required", 400

            task = images_dao.create(data)

            return jsonify(task), 201   

