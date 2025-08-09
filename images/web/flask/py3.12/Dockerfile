FROM docker.io/securityuniversal/web-apache:apache-2.4-2025.08
USER root
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip libapache2-mod-wsgi-py3 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir flask gunicorn
USER appuser
EXPOSE 8080
CMD ["bash","-lc","/usr/sbin/apachectl -DFOREGROUND"]
