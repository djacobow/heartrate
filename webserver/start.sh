#!/bin/sh


# To start the server:
# note that we only want one instance because this is a toy application
# using an in-memory "database" -- so it won't work right with multiple 
# threads
gunicorn \
   app \
   -w 1 \
   -b 127.0.0.1:8001 \


# now start the https terminator and reverse proxy nginx
sudo nginx 
# sudo nginx -s reload

