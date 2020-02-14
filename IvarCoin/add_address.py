import os
import requests
import pickle

list_ = ["http://0.0.0.0:8080/", "http://0.0.0.0:8081/", "http://0.0.0.0:8082/"]


def get_path():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "Data/node_id.txt")
    return file_path


with open(get_path(), "wb") as fp:
    pickle.dump(list_, fp)
