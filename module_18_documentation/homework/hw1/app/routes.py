import logging

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import Swagger, APISpec
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

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

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
api = Api(app)
spec = APISpec(
    title='BooksList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        """
       This is an endpoint for obtaining the books list.
       ---
       tags:
         - books
       responses:
         200:
           description: Books data
           schema:
             type: array
             items:
               $ref: '#/definitions/Book'
           """
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        """
        This is create book method
        ---
        tags:
         - books
        responses:
            200:
                 description: A single book item
        """
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
        """
        Book by id
        ---
        tags:
            - books
        responces:
             description: A single book
        """
        schema = BookSchema()
        return schema.dump(get_book_by_id(id)), 200

    def put(self, id):
        """
        Метод редактирования книги
        ---
        tags:
            - books
        responces:
             description: A single book
        """
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
        """
        Метод удаления книги
        ---
        tags:
            - books
        responces:
            код 204
        """
        delete_book_by_id(id)
        return '', 204


class AuthorList(Resource):
    def post(self):
        """
        Метод добавления автора книги
        ---
        tags:
            - authors
        responces:
            Моделька автора
        """
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
        """
        Метод получения автора по идентификатору
        ---
        tags:
            - authors
        responces:
            Автор
        """
        schema = AuthorSchema()
        return schema.dump(get_author_by_id(id)), 200

    def delete(self, id):
        """
        Метод удаления автора из базы
        ---
        tags:
            - authors
        responces:
            код 204
        """
        delete_author_by_id(id)
        return '', 204


template = spec.to_flasgger(
    app,
    definitions=[BookSchema],
)

swagger = Swagger(app)
api.add_resource(BookList, '/api/books')
api.add_resource(Book, '/api/books/<string:id>')
api.add_resource(Author, '/api/authors/<string:id>')
api.add_resource(AuthorList, '/api/authors')
if __name__ == '__main__':
    init_db(initial_records=DATA)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
