from Scripts.BlockChainApi import app, start_up
from flask_script import Manager, Server

startup_peers = ["http://0.0.0.0:8081/", "http://0.0.0.0:8082/", "http://0.0.0.0:8080/"]


manager = Manager(app)
server = Server(host="0.0.0.0")
manager.add_command("runserver", Server())
manager.add_command("start_up", start_up(startup_peers))

if __name__ == "__main__":
    manager.run()