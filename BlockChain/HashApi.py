from flask import Flask, request
from BlockChain.Datastructures import Element

app = Flask(__name__)
e = Element()


@app.route("/api/create_10/", methods=["GET"])
def create_10():
    random_value = ["0", "2", "42", "52", "25", "34", "77", "21", "75", "73"]
    for a in random_value:
        e.add_element(a)

    x = e.get_all()
    response = {"data": x}
    return response


@app.route('/api/', methods=["GET"])
def get_hash():
    x = e.get_all_hashes()
    response = {"Hashes": x}
    return response


@app.route("/api/add_data/", methods=["POST"])
def add_data():
    print("Yes")
    data = request.json["data"]
    print(data)
    print("------------------------------------", data)
    e.add_element(data)

    response = {"Data": e.get_all()}
    return response


@app.route("/api/get/all/", methods=["GET"])
def get_all():
    x = e.get_all()
    response = {"data": x}
    return response


@app.route("/api/get/first/", methods=["GET"])
def get_first():
    x = e.get_first()
    response = {"data": x}
    return response


@app.route("/api/get/last/", methods=["GET"])
def get_last():
    x = e.get_last()
    response = {"data": x}
    return response


@app.route("/api/get/by_index/", methods=["POST"])
def get_by_index():
    index = request.json["index"]
    x = e.get_by_index(index)
    response = {"data": x}
    return response


if __name__ == '__main__':
    app.run()
