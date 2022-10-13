import flask
from flask import *
import json, time
import pickle
import pandas as pd
from flask_cors import CORS,cross_origin
def recommend(book):
    book_index = books[books['isbn13'] == book].index[0]
    distances = similarity[book_index]
    books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_books = []
    recommended_books_covers = []
    for i in books_list:
        recommended_books.append(books.iloc[i[0]].title)
        recommended_books_covers.append(books.iloc[i[0]].thumbnail)
    return recommended_books, recommended_books_covers


books_dict = pickle.load(open('list (1).pkl', 'rb'))
books = pd.DataFrame(books_dict)

similarity = pickle.load(open('book_similar.pkl', 'rb'))

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
# @cross_origin(supports_credentials=True)
def homepage():
    data_set = {'page': 'home', 'time': time.time()}
    json_dump = json.dumps(data_set)
    return json_dump



# @app.route('/request/', methods=['GET'])
# @cross_origin()
# def requestquery():
#     selected_bookname = int(request.args.get('book'))
#     print(selected_bookname)
#     bookname , bookcover = recommend(selected_bookname)
#     data_set = flask.jsonify({'bookname':f'{bookname}','cover':f'{bookcover}'})
#     # json_dump = json.dumps(data_set)
#     data_set.headers.add('Access-Control-Allow-Origin','*')
#     return data_set

# @cross_origin(supports_credentials=True)

CORS(app)
@app.route('/request/', methods=['GET'])
def requestquery():
    selected_bookname = int(request.args.get('book'))
    print(selected_bookname)
    bookname , bookcover = recommend(selected_bookname)
    data_set = flask.jsonify(bookname=bookname,cover=bookcover)
    # json_dump = json.dumps(data_set)
    data_set.headers.add('Content-Type', 'application/json')
    data_set.headers.add('Access-Control-Allow-Origin', '*')

    # data_set.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    # data_set.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    # data_set.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
    return data_set


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
