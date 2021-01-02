from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item" : item}, 200 if item else 404
    
    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message" : f"An item with name {name} already exist."}
        
        data_post = Item.parser.parse_args()

        item = {
            "name" : name,
            "price" : data_post["price"]
        }
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message" : "Item deleted."}
    
    def put(self, name):
        data_put = Item.parser.parse_args()
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {
                "name" : name,
                "price" : data_put["price"]
            }
            items.append(item)
        else:
            item.update(data_put)
        return item

class ItemList(Resource):
    def get(self):
        return {"items" : items}