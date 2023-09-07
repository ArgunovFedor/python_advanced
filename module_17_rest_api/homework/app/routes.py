from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id, get_author_by_id, delete_author_by_id, add_author,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class Book(Resource):
    def get(self, id):
        schema = BookSchema()
        return schema.dump(get_book_by_id(id)), 200

    def put(self, id):
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        if get_book_by_id(id):
            book.id = id
            update_book_by_id(book)
        else:
            return '', 404
        return schema.dump(book), 200

    def delete(self, id):
        delete_book_by_id(id)
        return '', 204


class AuthorList(Resource):
    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return schema.dump(author), 201


class Author(Resource):
    def get(self, id):
        schema = AuthorSchema()
        return schema.dump(get_author_by_id(id)), 200

    def delete(self, id):
        delete_author_by_id(id)
        return '', 204


api.add_resource(BookList, '/api/books')
api.add_resource(Book, '/api/books/<string:id>')
api.add_resource(Author, '/api/authors/<string:id>')
api.add_resource(AuthorList, '/api/authors')
if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
