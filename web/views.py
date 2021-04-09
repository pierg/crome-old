from werkzeug.exceptions import HTTPException, NotFound, abort
from flask import render_template
from web import app

# App main route + generic routing
@app.route('/', defaults={'path': 'index'})
@app.route('/<path>')
def index(path):
    try:
        return render_template('layouts/default.html',
                               content=render_template('pages/' + path + ".html"))
    except:
        abort(404)
