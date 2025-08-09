FROM docker.io/securityuniversal/web-apache:apache-2.4-2025.08

USER root
# add python + venv + mod_wsgi (Apache module)
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip python3-venv libapache2-mod-wsgi-py3 \
    && rm -rf /var/lib/apt/lists/*

# create venv and install your Python deps there
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir flask gunicorn

# make venv binaries available in PATH
ENV PATH="/opt/venv/bin:${PATH}"

# tell mod_wsgi to use that venv (so your app imports the right site-packages)
# adjust 'user=appuser group=appuser' and python-path to your app as needed
RUN bash -lc 'cat > /etc/apache2/conf-available/flask-wsgi.conf <<EOF
WSGIDaemonProcess flaskapp user=appuser group=appuser threads=5 \
  python-home=/opt/venv
WSGIScriptAlias / /var/www/flaskapp.wsgi

<Directory /var/www/>
    Require all granted
</Directory>
EOF
a2enconf flask-wsgi'

# example WSGI entrypoint (adjust to your app)
RUN bash -lc 'cat > /var/www/flaskapp.wsgi <<EOF
from flask import Flask
app = Flask(__name__)
@app.get("/")
def hello():
    return "ok"
application = app
EOF'

USER appuser
EXPOSE 8080
CMD ["bash","-lc","/usr/sbin/apachectl -DFOREGROUND"]
