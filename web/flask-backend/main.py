import flask
import sys
import subprocess

from flask import render_template, request

app = flask.Flask("__main__")


@app.route("/")
def my_index():
    return flask.render_template("index.html", token="Hello Flask+React")


@app.route("/example/", methods=['POST'])
def run_example():
    # Moving forward code
    example_name = request.form['exampleButtons']
    result = subprocess.check_output([sys.executable, "..\\..\\examples\\running_example"
                                                      "\\" + example_name + ".py"])
    return render_template('index.html', result=result)


app.run(debug=True)
