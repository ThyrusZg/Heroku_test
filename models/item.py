from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # item model will now hold store id, we can link them
    # we can find in table 'store' column 'id' id that matches id in item
    store = db.relationship('StoreModel')  # reference

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # we use cls instead of ItemModel
        # SELECT * FROM items WHERE name=name LIMIT 1 (2nd name is argument) - It returns ItemModel object

    def save_to_db(self):  # it is insert and update in the same (upsert)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
