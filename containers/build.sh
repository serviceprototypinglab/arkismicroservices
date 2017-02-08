#!/usr/bin/env bash
docker build -t chumbo/arkisbackend:2.0.2 ./Backend
docker build -t chumbo/arkisfrontend:2.0.3 ./Frontend
docker-compose up