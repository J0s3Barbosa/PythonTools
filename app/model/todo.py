# import mongoengine

# class Todo(mongoengine.Document):
    
#     title = mongoengine.StringField()
#     description = mongoengine.IntField()
#     done = mongoengine.StringField()

class Todo:
    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done
