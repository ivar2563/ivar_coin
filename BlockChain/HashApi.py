from flask import Flask, request
from BlockChain.Datastructures import Element
from BlockChain.CheckWork import validate

app = Flask(__name__)
e = Element()


@app.route("/api/create_10/", methods=["GET"])
def create_10():
    """
    Wont work
    Will create 10 nodes
    :return:
    """
    random_value = ["0", "2", "42", "52", "25", "34", "77", "21", "75", "73"]
    for a in random_value:
        e.add_element(a)

    x = e.get_all()
    response = {"data": x}
    return response


@app.route('/api/', methods=["GET"])
def get_hash():
    """
    :return:
    """
    x = e.get_all_hashes()
    response = {"Hashes": x}
    return response


@app.route("/api/add_node/", methods=["POST"])
def add_node():
    """
    Will add a node
    it needs proof of work string
    for now it needs some sort of data
    :return:
    """
    string_ = request.json["string"]
    data = request.json["data"]
    string_response = validate(string_)
    if string_response is True:
        response = e.add_element(data, string_)
        return response, 200
    else:
        return "The string was already used, or its wrong", 400


@app.route("/api/get/all/", methods=["GET"])
def get_all():
    """
    Will get all of the nodes
    :return:
    """
    x = e.get_all()
    response = {"data": x}
    return response


@app.route("/api/get/first/", methods=["GET"])
def get_first():
    """
    Will get the first element in the chain
    :return:
    """
    x = e.get_first()
    response = {"data": x}
    return response


@app.route("/api/get/last/", methods=["GET"])
def get_last():
    """
    Will get the last elemnt in the chain
    :return:
    """
    x = e.get_last()
    response = {"data": x}
    return response


@app.route("/api/get/by_index/", methods=["POST"])
def get_by_index():
    """
    Will most likely be removed

    :return:
    """
    index = request.json["index"]
    x = e.get_by_index(index)
    response = {"data": x}
    return response


if __name__ == '__main__':
    app.run()
    x = Element()
    x.validate_chain()
