from datetime import datetime
from functools import reduce
from typing import List
import re

import numpy as np
from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, Email, NumberRange, Regexp

app = Flask(__name__)


@app.route(
    "/search/", methods=["GET"],
)
def search():
    cell_tower_ids: List[int] = request.args.getlist("cell_tower_id", type=int)

    if not cell_tower_ids:
        return f"You must specify at least one cell_tower_id", 400

    phone_prefixes: List[str] = request.args.getlist("phone_prefix")

    protocols: List[str] = request.args.getlist("protocol")

    signal_level: Optional[float] = request.args.get(
        "signal_level", type=float, default=None
    )
    date_from: datetime = datetime.strptime(request.args.get('date_from'), '%Y-%m-%d')
    date_to: datetime = datetime.strptime(request.args.get('date_to'), '%Y-%m-%d')
    if date_to < date_from:
        return 'date_to >= date_from', 400

    if any(x < 0 for x in cell_tower_ids):
        return 'Каждый cell_tower_id должен быть больше 0', 400

    if any(x not in ['2G', '3G', '4G'] for x in protocols):
        return 'protocol может быть только 2G, 3G или 4G'
    print(phone_prefixes[len(phone_prefixes) - 1][-1])
    if sum([len(x) for x in phone_prefixes]) > 10 or phone_prefixes[len(phone_prefixes) - 1][-1] != '*':
        return 'phone_prefix должен состоять из чисел ' \
               'и заканчиваться звёздочкой ' \
               '(при этом чисел должно быть не больше, чем 10)', 400

    return (
        f"Search for {cell_tower_ids} cell towers. Search criteria: "
        f"phone_prefixes={phone_prefixes}, "
        f"protocols={protocols}, "
        f"signal_level={signal_level}"
        f"date_from={str(date_from)}"
        f"date_to={str(date_to)}"
    )


@app.route(
    "/array/", methods=["GET"],
)
def array():
    request_list: List[int] = request.args.getlist("arr", type=int)
    result_sum = sum(request_list)
    result_mult = np.prod(request_list)
    return (
        f'summ {result_sum} '
        f'mult {result_mult}'
    )

@app.route('/sum/', methods=['GET'])
def search2():
    try:
        items: List[int] = request.args.getlist('item', type=int)
        if not items:
            return f'<h2>Data must be in {items}</h2>', 400
        my_sum = sum(items)
        my_compos = reduce(lambda x, y: x*y, items)
    except Exception as message:
        return f'<h1>{message}</h1>', 400

    return (
        f'<h2>For array {items}:</h2>'
        f'<p>my_sum={my_sum}</p>'
        f'<p>my_compos={my_compos}</p>'
    )


@app.route(
    "/sum/", methods=["POST"],
)
def _sum():
    arrays: List[int] = request.get_json()
    result = ','.join(str(a1 + a2) for (a1, a2) in zip(arrays['array1'], arrays['array2']))
    return (
        f'summ {result}'
    )


class RegistrationForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    phone = IntegerField('Phone: ', validators=[NumberRange(min=0, max=9999999999, message='Длина номера телефоне не должно превышать 10 символов')])
    name = StringField("Name: ", validators=[Regexp(regex='\A([a-zA-Zа-яА-Я]{1,20}) \w{1}[.]{1}\w{1}[.]{1}$', message='Введите имя в формате Фамилия И.О.')])
    address = StringField()
    index = IntegerField()
    comment = StringField()

@app.route('/registration/', methods=['POST'])
def registartion():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data
        return f'Successfully registered user {email} with phone +7{phone}'
    errors = ''
    for parameter_name, value_list in form.errors.items():
        errors += parameter_name + '=' + ' '.join(value_list)
        errors += '\n'
    return f'{errors}', 400

class CustomModel(FlaskForm):
    name = StringField(validators=[DataRequired()])
    family_name = StringField(validators=[DataRequired()])
    number = IntegerField(validators=[NumberRange(100000, 999999, 'Номер должен быть из 6 чисел и первое число не должно быть равен 0')])


@app.route('/custom/', methods=['POST'])
def custom_endpoint():
    form = CustomModel()

    if form.validate_on_submit():
        number, name, family_name = form.number.data, form.name, form.family_name
        first_three_number = 0
        for i in str(number // 1000):
            first_three_number += int(i)

        last_three_number = 0
        for i in str(number % 1000):
            last_three_number += int(i)

        if first_three_number == last_three_number:
           return f"Поздравляем вас {name} {family_name}"
        else:
            return "Неудача. Попробуйте ещё раз!"
    errors = ''
    for parameter_name, value_list in form.errors.items():
        errors += parameter_name + '=' + ' '.join(value_list)
        errors += '\n'
    return f"Invalid input, {form.errors}", 400

if __name__ == "__main__":
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
