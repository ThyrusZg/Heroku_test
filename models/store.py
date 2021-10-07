from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # back reference, it allows the store to see which items are
    # in items table with store id equal to its own id  (many to one relationship - one store with many items)
    # lazy=dynamic will not go to items table and create object for each item

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        # .all() we need because lazy=dynamic. self.items is query builder that has ability to look in items table.

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):  # it is insert and update in the same (upsert)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
