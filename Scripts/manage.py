from abc import ABC

from Scripts.BlockChainApi import app, start_up
from flask_script import Manager, Server


def start():
    startup_peers = ["http://0.0.0.0:5000/", "http://0.0.0.0:8081/", "http://0.0.0.0:8082/", "http://0.0.0.0:8080/"]
    start_up(startup_peers)


class CustomServer(Server, ABC):
    def __call__(self, app, *args, **kwargs):
        start()

        return Server.__call__(self, app, *args, **kwargs)


manager = Manager(app)
manager.add_command("runserver", CustomServer())

if __name__ == "__main__":
    manager.run()
