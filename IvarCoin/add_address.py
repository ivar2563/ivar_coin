import os
import requests
import pickle



def get_path():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "Data/peer_list.txt")
    return file_path

list_ = ["http://0.0.0.0:8080/", "http://0.0.0.0:8081/", "http://0.0.0.0:8082/", "http://localhost:5000/"]


with open(get_path(), "wb") as fp:
    pickle.dump(list_, fp)
