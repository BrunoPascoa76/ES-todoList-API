#!/bin/bash

docker build -t todolist .
docker run -dp 5000:5000 -v ./app:/app todolist