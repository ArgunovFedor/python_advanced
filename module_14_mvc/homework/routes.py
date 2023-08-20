from flask import Flask, render_template, request
from typing import List

from models import init_db, get_all_books, DATA, add_book

app: Flask = Flask(__name__)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> str:
    if request.method == 'POST':
        author = request.form.get('author_name')
        book = request.form.get('book_title')
        if author is not None and book is not None:
            add_book(author, book)
        return render_template('add_book.html')
    else:
        return render_template('add_book.html')


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
