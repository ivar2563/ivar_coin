from flask import Flask, request
from IvarCoin.BlockChain import Element
from IvarCoin.CheckWork import validate_
import logging

app = Flask(__name__)
e = Element()


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
    string_response = validate_(string_)
    if string_response is True:
        response = e.add_element(data, string_)
        logging.debug(response)
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


@app.route("/api/get_node/", methods=["POST"])
def get_node_with_receipt():
    """
    Will get the node associated with the receipt
    :return:
    """
    receipt = request.json["receipt"]
    node = e.get_node(receipt)
    return node


if __name__ == '__main__':
    app.run()
    x = Element()
    x.validate_chain()
