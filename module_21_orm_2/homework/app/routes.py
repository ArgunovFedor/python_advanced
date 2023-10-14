from flask import Flask, request
from flask_restful import Api, Resource

from module_20_orm_1.homework.app.models import Book, ReceivingBook, Student
from module_20_orm_1.homework.app.schemas import BookSchema, StudentSchema, ReceivingBookSchema

app = Flask(__name__)
api = Api(app)


@app.route('/api/students/debtors', methods=['GET'])
def debtors():
    result = []
    debtors = ReceivingBook.get_debtors()
    for debtor in debtors:
        result.append(Student.get_by_id(debtor.student_id))
    schema = StudentSchema()
    return schema.dump(result, many=True), 200


@app.route('/api/books/give_to_student', methods=['POST'])
def give_to_student():
    book_id = request.args.get('book_id')
    id_student = request.args.get('id_student')
    schema = ReceivingBookSchema()
    item = ReceivingBook.give_to_student(id_book=book_id, id_student=id_student)
    return schema.dump(item), 200


@app.route('/api/books/hand_over_the_book', methods=['POST'])
def hand_over_the_book():
    book_id = request.args.get('book_id')
    id_student = request.args.get('id_student')
    schema = ReceivingBookSchema()
    item = ReceivingBook.hand_over_the_book(id_book=book_id, id_student=id_student)
    return schema.dump(item, many=True), 200


@app.route('/api/book/by_authors/<id>', methods=['GET'])
def get_by_author_id(id: int):
    '''
    получите количество оставшихся в библиотеке книг по автору (GET — входной параметр — ID автора);
    '''
    author_id = id
    schema = BookSchema()
    item = Book.get_all_books_by_author(author_id=author_id)
    return schema.dump(item, many=True), 200


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        books = Book.get_all_books()
        return schema.dump(books, many=True), 200


api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    app.run(debug=True)
