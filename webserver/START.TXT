# To start the server:
# NB: gunicorn is designed to run behing a reverse proxy like nginx,
# so this is a bit unsafe 
gunicorn \
   app \
   -b 0.0.0.0:8000 \
   -D

