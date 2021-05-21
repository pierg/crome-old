from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
from os import path

if path.exists('../frontend/build'):
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
else:
    app = Flask(__name__)

CORS(app)
api = Blueprint('api', __name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@api.route('/submit', methods=['POST'])
def handle_submit():
    if request.method == "POST":
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        job = request.form['job']
        print(f'first name : {first_name}')
        print(f'last name : {last_name}')
        print(f'job : {job}')

        # do your processing logic here.

        return jsonify({
            "firstName": first_name,
            "lastName": last_name,
            "job": job
        })


app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
