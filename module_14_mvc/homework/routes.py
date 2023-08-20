from flask import Flask, render_template, request
from typing import List
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Email, NumberRange, Regexp, InputRequired
from models import init_db, get_all_books, DATA, add_book, get_all_books_by_author

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


class AddBookWithAuthorForm(FlaskForm):
    author = StringField(name='author_name', validators=[InputRequired()])
    book = StringField(name='book_title', validators=[InputRequired()])


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(),
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> str:
    if request.method == 'POST':
        form = AddBookWithAuthorForm()
        if form.validate_on_submit():
            author = form.author.data
            book = form.book.data
            if author is not None and book is not None:
                add_book(author, book)
        else:
            return render_template('add_book.html', form=form)
    else:
        return render_template('add_book.html')


@app.route('/books/author')
def all_books_by_author() -> str:
    author = request.args.get('author')
    return render_template(
        'books_by_author.html',
        books=get_all_books_by_author(author)
    )


if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    init_db(DATA)
    app.run(debug=True)
