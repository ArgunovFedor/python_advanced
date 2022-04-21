import datetime
import random
import string

from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def test_function():
    return 'Привет мир!'


@app.route('/cars')
def cars():
    return 'Chevrolet, Renault, Ford, Lada'


cats_list = ['корниш рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']


@app.route('/cats')
def cats():
    global cats_list
    return str(random.choice(cats_list))


@app.route('/get_time/now')
def get_time_now():
    return str(datetime.datetime.now())


@app.route('/get_time/future')
def get_time_future():
    return str(datetime.datetime.now() + datetime.timedelta(hours=1))


count = 0

@app.route('/counter')
def counter():
    global count
    count += 1
    return str(count)


tab = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

war_and_peace = open('war_and_peace.txt', 'r', encoding='utf-8') \
    .read() \
    .translate(tab) \
    .split()


@app.route('/get_random_word')
def get_random_word():
    global war_and_peace
    return random.choice(war_and_peace)


app.run(debug=True, host='localhost', port=8080)
