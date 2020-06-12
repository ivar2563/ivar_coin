# Ivar_coin

* If you want to test the program, run the file "manage.py" with the parameters "runserver -h 0.0.0.0"
* Start of the program with building the docker image with "docker build -t ivarcoin .". run the powershell script. When done run manage.py
* To send api calls us the file "StressTest.py" or "GetNodeTest.py"
    * The first time you will most likely have to run the script more then once
* The "UnitTest.py" will not work if the chain is empty

#### The lattes push don't work 
* The current way to start the first node is in pycharm. After that you need to get the ip of the node in "chain.log",
go to the Dockerfile and change the python parameter to the ip. Then you need to build the docker image, 
when that is done you can run the powershell script called "docker_node_setup.ps1"


## For later development 
* The main issue of the current program is the docker aspect, and the host and port.
* Missing aspect in the validating of chains. In current version it would be extremely easy to manipulate the chain 

## Docker
* docker build -t ivarcoin .

* docker run -d -p 8080:5000 \
  --name=ivarcoin \
  --mount source=ivarcoin-vol,destination=/app/IvarCoin/Data \
  ivarcoin:latest
  
 https://docs.docker.com/storage/volumes/
 
 ### Delete volume
* docker volume ls 
* docker volume rm (volume name) 