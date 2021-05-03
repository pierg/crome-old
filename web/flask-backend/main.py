import flask
import sys
import subprocess

from flask import render_template, request
from pathlib import Path

app = flask.Flask("__main__")


@app.route("/")
def my_index():
    return flask.render_template("index.html", token="Hello Flask+React")


@app.route("/example/", methods=['POST'])
def run_example():
    # Moving forward code
    example_name = request.form['exampleButtons']
    output_path = "../../examples/running_example/" + example_name + ".py"
    output_path = Path(output_path)
    result = subprocess.check_output([sys.executable, output_path])
    return render_template('index.html', result=result)


app.run(debug=True)
