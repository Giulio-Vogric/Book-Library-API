from db import db


class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    num_of_pages = db.Column(db.Integer)
    price = db.Column(db.Float(precision=2))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel')

    def __init__(self, name, num_of_pages, price, category_id):
        self.name = name
        self.num_of_pages = num_of_pages
        self.price = price
        self.category_id = category_id

    def json(self):
        return {'name': self.name,
                'num_of_pages': self.num_of_pages,
                'price': self.price,
                'category_id': self.category_id
                }

    @classmethod
    def find_by_name(cls, name):
        return BookModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(id):
        return BookModel.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
