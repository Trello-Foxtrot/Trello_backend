# Trello_backend
pip install django-sslserver
python manage.py runsslserver --certificate cert.pem --key key.pem

https://github.com/FiloSottile/mkcert/releases
mkcert -cert-file cert.pem -key-file key.pem localhost
