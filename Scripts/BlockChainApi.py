from flask import Flask, request
from IvarCoin.BlockChain import Element
from IvarCoin.CheckWork import validate_
import requests
from threading import Thread, Lock
import logging
import time
import socket
import sys


peer_list = []
app = Flask(__name__)

e = Element(peer_list)
global node_address
node_address = ""
startup_peers = []


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
        data = {"string": string_, "data": response, "node_address": request.host_url}
        for peer_ip in peer_list:
            connection = peer_ip.replace("0.0.0.0", "localhost")
            peer_connection = connection + "register/chain/"
            try:
                x = requests.post(peer_connection, json=data)
                logging.debug("")
            except Exception:
                logging.critical(sys.exc_info())
                pass

        return list(response.keys())[0], 200

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
    Will get the last element in the chain
    :return:
    """
    response = {"data": e.get_last()}
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


@app.route("/register/new_peer/", methods=["POST"])
def register_new_peer():
    """
    Not in use
    :return:
    """
    peer_address = request.json["data"]
    print(peer_address)
    if peer_address:
        if peer_address not in peer_list:
            response = {"data": peer_list}
            peer_list.append(peer_address)
            return response, 200
        else:
            return "Already added", 400
    else:
        return "Node address not there", 400


@app.route("/register/exiting_peer/", methods=["GET"])
def existing_peer():
    """
    This api function will send a chain dump with the length of the chain, its used to validate nodes

    :return:
    """
    own_address = request.host_url
    data = {"node_address": own_address}
    print("peer ", own_address)
    data1 = {
        "chain": e.get_all(),
        "length": len(e.get_all())
    }
    if not own_address:
        return "something went wrong", 400
    else:
        for peer in peer_list:
            try:
                if "0.0.0.0" in peer:
                    peer = peer.replace("0.0.0.0", "localhost")

                print(peer + "register/new_peer/")
                response = requests.post(peer + "register/new_peer/", json=data)
                if response.status_code == 200:
                    if type(response.content) == list:
                        for p in response.content:
                            if p not in peer_list:
                                peer_list.append(p)
            except ConnectionError as _:
                print(_)
                pass

        return data1, 200


@app.route("/test/", methods=["GET"])
def test():
    """
    Not in use
    :return:
    """
    x = requests.get(request.host_url + "register/exiting_peer/")
    print(x)
    return x.content, 200


@app.route("/chain_dump/", methods=["POST"])
def send_chain():
    """
    Not in use
    :return:
    """
    node_address = request.remote_addr
    print(node_address)
    if node_address:
        peer_list.append(node_address)
        return e.get_all()
    else:
        return "No valid address given"


@app.route("/register/chain/", methods=["POST"])
def register_new_chain_element():
    """
    When a new element is sendt to a node, the add node function will send this api call to every peer in the peer list
    :return:
    """
    data = request.json["data"]
    string = request.json["string"]
    address = request.json["node_address"]
    if address not in peer_list:
        peer_list.append(address)
    if not data or not string:
        return "No data/string was found with the request", 400
    else:
        address = request.remote_addr
        temp_list = peer_list
        if address in temp_list:
            temp_list.remove()
        if address not in temp_list:
            peer_list.append(address)
        logging.debug(address)
        temp_list.remove(address)
        e.add(data, string, state=True)
        return "Success", 200


@app.route("/test_connection/", methods=["GET"])
def test_connection():
    """
    Is used to check if a node is still alive and able to recive calls, if it dont return a 200 status code
    it wil be removed from the requesting peer
    :return:
    """
    return "still a active peer", 200


@app.route("/test2/", methods=["GET"])
def test2():
    """
    Not in use
    :return:
    """
    x = request.host_url
    return x


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()
host = '0.0.0.0'


def start_up(startup_peers):
    """
    First function to run after the api, will get a list of peers from known nodes

    :param startup_peers:
    :return:
    """
    data = {"data": "http://{}:{}/".format(host, port)}
    for peer in startup_peers:
        print(peer)
        try:
            logging.debug("start")
            if "0.0.0.0" in peer:
                peer = peer.replace("0.0.0.0", "localhost")
            x = peer + "register/new_peer/"
            logging.debug("over requests")
            r = requests.post(x, json=data)
            logging.debug("after requests")
            response = dict(r.json())
            logging.debug("after")
            logging.debug("mid")
            if int(r.status_code) == 200 and isinstance(response, dict):
                logging.debug(peer)
                if peer not in peer_list:
                    peer_list.append(peer)
                logging.debug("end")
                for a in response["data"]:
                    if a not in startup_peers:
                        peer_list.append(a)
            else:
                logging.debug("One of the startup nodes did not respond or it did not work")
        except OSError:
            logging.critical("Startup failed, node is useless")
            print("Unexpected error:", sys.exc_info())
            pass


def beat():
    """
    Will check chain size with other nodes, if this node is smaller then the other node it will change it out with the a
    chain that most the other nodes use

    Need to implement a way to recognise know good nodes
    :return:
    """
    logging.debug("heartbeat started")
    mutex = Lock()
    mutex.acquire()
    saved_chain = {}
    num = 1
    for peer in peer_list:
        try:
            test_if_alive = requests.get("http://{data}test_connection/".format(data=peer))
            if test_if_alive.status_code == 200:
                remote_chain = requests.get("http://{data}register/exiting_peer/".format(data=peer))
                x = dict(remote_chain.reponse)
                if len(e.get_all()) < int(x["length"]):

                    if saved_chain == {}:
                        saved_chain.update({1: {"chain": x["chain"], "identical": 1}})
                    else:
                        for a in range(num):
                            if saved_chain[a + 1] == x["chain"]:
                                saved_chain[a + 1]["identical"] += 1
                                break
                            else:
                                num += 1
                                saved_chain.update({a + 1: {"chain": x["chain"], "identical": 1}})
                                break
                if len(e.get_all()) == int(x["length"]):
                    pass
            else:
                peer_list.remove(peer)

        except OSError:
            logging.debug(sys.exc_info())
    if saved_chain != {}:
        print(saved_chain)
        current_chain = {}
        for id in range(num):
            identical = saved_chain[id + 1]["identical"]
            chain = saved_chain[id + 1]["chain"]
            if current_chain == {}:
                current_chain = {"chain": chain, "identical": identical}
            if current_chain["identical"] >= identical:
                current_chain = {"chain": chain, "identical": identical}
        # replace chain

    mutex.release()
    logging.debug("heartbeat ended")


class FlaskThread(Thread):
    def run(self):
        app.run(host=host, port=port)


def heart_beat():
    while not heart_beat.cancelled:
        beat()
        time.sleep(30)


heart_beat.cancelled = False


def main():
    start_addresses = sys.argv
    start_addresses.remove(start_addresses[0])
    if len(start_addresses) >= 1:
        if len(start_addresses) > 1:
            for address in start_addresses:
                startup_peers.append(address)
        else:
            startup_peers.append(start_addresses[0])
    server = FlaskThread()
    server.daemon = True
    server.start()
    time.sleep(2)
    start_up(startup_peers)
    t = Thread(target=heart_beat())
    server.join()
    t.start()
    heart_beat.cancelled = True


if __name__ == "__main__":
    main()
