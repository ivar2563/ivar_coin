$nodes = 3
for ($i=0; $i -lt $nodes ;$i++){
docker run -d -p "808$($i):5000" --mount target=/app/IvarCoin/Data ivarcoin:latest
}



#--mount source="ivarcoin$($i)-vol",target=/app/IvarCoin/Data ivarcoin:latest
    