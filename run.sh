docker run -d -it --net=host --link sithmail-redis:redis --name $1 -v "$PWD":/usr/src/legobot -w /usr/src/legobot legobot
