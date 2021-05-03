import flask
import sys
import subprocess

from flask import render_template

app = flask.Flask("__main__")


@app.route("/")
def my_index():
    return flask.render_template("index.html", token="Hello Flask+React")


@app.route("/example/", methods=['POST'])
def run_example():
    # Moving forward code
    result = subprocess.check_output([sys.executable, "..\\..\\examples\\running_example"
                                                      "\\1_analysis_build_cgg.py"])
    return render_template('index.html', result=result)



app.run(debug=True)
