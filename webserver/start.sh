#!/bin/sh


# To start the server:
# NB: gunicorn is designed to run behing a reverse proxy like nginx,
# so this is a bit unsafe 
gunicorn \
   app \
   -b 127.0.0.1:8000 \


# now start nginx
nginx 
