from flask_restful import Resource, reqparse
from models.book import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='The price field cannot be left blank.')
    parser.add_argument('num_of_pages',
                        type=int,
                        required=False,
                        help='The Number of pages field can be left blank.')
    parser.add_argument('category_id',
                        type=float,
                        required=True,
                        help='Every book needs to be assigned to a category.')

    def get(self, name):
        book = BookModel.find_by_name(name)
        return book.json() if book else {'message': 'Book not found'}, 404

    def post(self, name):
        if BookModel.find_by_name(name):
            return {'message':
                    "A book with name '{}' already exist".format(name)}, 400
        data = Book.parser.parse_args()
        book = BookModel(name, **data)
        try:
            book.save_to_db()
        except:
            return {'message': 'A server error occured. Try again in a bit.'}, 500
        return book.json()

    def put(self, name):
        data = Book.parser.parse_args()
        book = BookModel.find_by_name(name)
        if book is None:
            book = BookModel(name, **data)
        else:
            book.price = data['price']
            book.category_id = data['category_id']
        book.save_to_db()
        return book.json()

    def delete(self, name):
        book = BookModel.find_by_name(name)
        if book:
            book.delete_from_db()
        return {'message': 'item deleted'}


class BookList(Resource):
    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}
