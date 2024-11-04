#!/bin/bash

docker build -t todolist .
docker run -dp 5000:5000 --env-file=.env -v ./app:/app todolist