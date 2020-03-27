from Scripts.BlockChainApi import app, start_up
from flask_script import Manager, Server

manager = Manager(app)


@manager.command
def start():
    startup_peers = ["http://0.0.0.0:8081/", "http://0.0.0.0:8082/", "http://0.0.0.0:8080/"]
    start_up(startup_peers)


server = Server(host="0.0.0.0")
manager.add_command("runserver", Server())

if __name__ == "__main__":
    manager.run()
