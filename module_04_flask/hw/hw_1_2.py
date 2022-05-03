"""
В /registration endpoint добавьте все валидаторы,
о которых говорилось на последнем уроке:
    1) email (обязательно для заполнение, валидация формата),
    2) phone (обязательно для заполнения, длина 10 символов, только числа),
    3) name (обязательно для заполнения),
    4) address (обязательно для заполнения),
    5) index (только числа, обязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Email, NumberRange, Regexp

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    phone = IntegerField(validators=[DataRequired(), NumberRange(1000000000, 9999999999)])
    name = StringField(validators=[DataRequired()])
    address = StringField(validators=[DataRequired()])
    index = IntegerField(validators=[DataRequired()])
    comment = StringField(validators=[DataRequired()])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
