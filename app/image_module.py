# coding=utf-8
import json
from flask import jsonify, request, Blueprint
from app.image import ImagesDAO
import pymongo
from flask.templating import render_template
import numpy as np 
import cv2 
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
        
        # since the pyautogui takes as a  
        # PIL(pillow) and in RGB we need to  
        # convert it to numpy array and BGR  
        # so we can write it to the disk 
        image = cv2.cvtColor(np.array(image), 
                            cv2.COLOR_RGB2BGR) 
        file_name_timestr = time.strftime("%Y%m%d-%H%M%S")
        print(image_folder+ file_name_timestr+'.jpg')

        # writing it to the disk using opencv 
        cv2.imwrite(os.path.join(image_folder+ file_name_timestr+'.jpg') , image) 

        image_dao.insert_image(image)
        
        return 'GetScreenShot' 

    @imageModule.route('/CountScreenShot')
    def CountScreenShot():
        number_image = image_dao.retrieve_image()
        return number_image + 'images in database' 


