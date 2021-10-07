from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This filed cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': " An item with name '{}' already exists!".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])  # we can simplify data['price'], data['store_id']
        # with **data (unpacking) 

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}  # list comprehension, we take
        # item.json() for each item  in all ItemModel objects. query.all will find all ItemModel objects
        """
        Or if we want to use lambda, It would apply lambda x: x.json for each element in this list ItemModel.query.all()
        map is mapping of functions to elements and it would make it into the list.
        
        return {'items': list(map(lambda x: x.json , ItemModel.query.all()))}
        """