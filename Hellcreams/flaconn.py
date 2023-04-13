import base64
import json

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_data():
    data = request.json()
    return data

@app.route("/secret")
def secret():
    return "2"


@app.route("/new_con")
def send_image():
    with open("new_con/send_client_image.jpg", "rb") as f:
        image_bytes = f.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        response_data = {"image_data":base64_image}
        response = jsonify(response_data)

        return response


if __name__ == "__main__":
    app.run(debug=True)
