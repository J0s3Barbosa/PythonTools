# coding=utf-8
import base64
import pymongo
import json
from bson import json_util
from bson.objectid import ObjectId
from io import *

class ImagesDAO:

    def __init__(self, database):
        self.database = database
        self.image_collection = self.database.image

    def create(self, data):
        image = {
            'title': data.get('title'),
            'description': data.get('description'),
            'done': False
        }

        inserted_id = self.image_collection.insert_one(image).inserted_id
        image = self.image_collection.find_one({ '_id': ObjectId(inserted_id) })

        return self.to_json(image)

    def list(self):
        images = self.image_collection.find().sort('done', pymongo.ASCENDING)
        return self.to_json(images)

    def read(self, object_id):
        image = self.image_collection.find_one({ '_id': ObjectId(object_id)})
        return self.to_json(image)

    def update(self):
        pass

    def delete(self):
        pass

    def to_json(self, data):
        return json.loads(json_util.dumps(data))


    def insert_image_request(self,request):
        with open(request.GET["image_name"], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        abc= self.image_collection.insert({"image":encoded_string})
        return self.to_json("inserted")


    def insert_image(self,image):
        data = base64.b64encode(image)
        abc= self.image_collection.insert({"image":data})
        return self.to_json("inserted")
    
    def retrieve_image(self):
        data = self.image_collection.find()
        data1 = self.to_json(data)
        img = data1[0]['image'];
        binaryString = img['$binary']
        # image = Image.frombytes('RGBA', (800,600), str_bytes, 'raw')
        # image.show()
        imgdata = base64.b64decode(binaryString)

        img_tag = '<img alt="sample" src="data:image/jpeg;base64,{0}">'.format(imgdata)
        # data1 = base64.b64decode(binaryString)
        return imgdata
