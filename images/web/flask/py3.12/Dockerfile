FROM docker.io/securityuniversal/web-apache:apache-2.4-2025.08.P1

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip python3-venv libapache2-mod-wsgi-py3 \
    && rm -rf /var/lib/apt/lists/*

# Create venv and install deps (PEP 668-safe)
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir flask

# Write Apache mod_wsgi config without heredocs
RUN set -eux; \
  { \
    echo 'WSGIDaemonProcess flaskapp user=appuser group=appuser threads=5 python-home=/opt/venv'; \
    echo 'WSGIScriptAlias / /var/www/flaskapp.wsgi'; \
    echo '<Directory /var/www/>'; \
    echo '    Require all granted'; \
    echo '</Directory>'; \
  } > /etc/apache2/conf-available/flask-wsgi.conf \
  && a2enconf flask-wsgi

# Minimal WSGI entrypoint
RUN set -eux; \
  printf '%s\n' \
"from flask import Flask" \
"app = Flask(__name__)" \
"@app.get('/')" \
"def hello(): return 'ok'" \
"application = app" \
  > /var/www/flaskapp.wsgi

ENV PATH="/opt/venv/bin:${PATH}"
USER appuser
EXPOSE 8080
CMD ["bash","-lc","/usr/sbin/apachectl -DFOREGROUND"]
