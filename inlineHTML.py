import flask
import requests


app = flask.Flask(__name__)
counter = 0


@app.route("/")
def home():
    return "Hello! This is the main page <h1>Hello<h1>"


@app.route("/<name>")
def entry(name):
    return "Hello! This is the main page <h1>%s<h1>" % name


@app.route("/api/counter", methods=['POST'])
def server_count_increment():
    """Method to post and adjust the internal counter"""
    global counter
    content = flask.request.json
    add = content['add']
    print(f"Number to add: {add}")
    counter += add
    print(f"Counter is now: {counter}")
    return flask.jsonify({'counter': counter})


@app.route("/api/counter", methods=['GET'])
def server_get_count():
    global counter
    return flask.jsonify({'counter': counter})


if __name__ == "__main__":
    app.run(host="0.0.0.0")




