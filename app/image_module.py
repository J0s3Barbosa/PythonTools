# coding=utf-8
import json
from flask import jsonify, request, Blueprint
from app.image import ImagesDAO
import pymongo
from flask.templating import render_template
import numpy as np 
import pyautogui 
import time
import os
from app.config.app_config import mongo_config

imageModule = Blueprint('image', __name__,
                        template_folder='templates')

try:
    client = pymongo.MongoClient(
    mongo_config['connectionString']
    )
    database = client.image
    image_dao = ImagesDAO(database)
    ROOT_DIR = os.path.abspath(os.curdir)
    image_folder = ROOT_DIR+"\\images\\"

except Exception as exc:
    print(exc)
# log

class ImageModule():

    @imageModule.route('/images')
    def images():
        list = image_dao.retrieve_image()
        return render_template('images/image_index.html',data=list)


    @imageModule.route('/GetScreenShot')
    def GetScreenShot():
        # imagem = ImageGrab.grab()
        # imagem.save('screenShot1.jpg', 'jpeg')
        
        # take screenshot using pyautogui 
        image = pyautogui.screenshot() 
        image_dao.insert_image(image)
        
        return 'GetScreenShot' 

    @imageModule.route('/CountScreenShot')
    def CountScreenShot():
        number_image = image_dao.retrieve_image()
        return number_image + 'images in database' 


