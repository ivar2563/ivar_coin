# Ivar_coin

* If you want to test the program, run the file "HashApi.py"
* To send api calls us the file "StressTest.py" or "GetNodeTest.py"
    * The first time you will most likely have to run the script more then once
* The "UnitTest.py" will not work if the chain is empty

## Docker
* docker build -t ivarcoin .

* docker run -d -p 8080:5000 \
  --name=ivarcoin \
  --mount source=ivarcoin-vol,destination=/app/IvarCoin/Data \
  ivarcoin:latest
  
 https://docs.docker.com/storage/volumes/
 
 ### delete volume 
* docker volume ls 
* docker volume rm (volume name) 