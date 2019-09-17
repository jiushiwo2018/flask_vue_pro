from flask import Flask
from flask import make_response, jsonify

app = Flask(__name__)

def get_json():
    a = {"answer": "yes", "forced": False}

    response = make_response(jsonify(a))

    return  response


@app.route("/")
def hello_world():
    return get_json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)