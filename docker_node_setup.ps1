$nodes = 3

# Create first node
docker run -d -p "8080:5000" --mount target=/app/IvarCoin/Data ivarcoin:latest

# Create subsequent nodes
for ($i=1; $i -lt $nodes ;$i++){
  # Subsequent nodes will connect to first node
  docker run -d -p "808$($i):5000" -e "REMOTE_PORT=8000" --mount target=/app/IvarCoin/Data ivarcoin:latest
}