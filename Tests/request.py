import requests


def test():
    x = requests.get("http://localhost:8080/test_connection/")
    print(x.status_code)
    print(x.text)


test()