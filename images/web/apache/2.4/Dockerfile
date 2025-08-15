FROM docker.io/securityuniversal/base-ubuntu:24.04-2025.08.P15
USER root
RUN apt-get update && apt-get install -y --no-install-recommends apache2 apache2-utils && rm -rf /var/lib/apt/lists/*
RUN usermod -a -G www-data appuser && chown -R appuser:www-data /var/www
USER appuser
EXPOSE 8080
CMD ["bash","-lc","/usr/sbin/apachectl -DFOREGROUND"]
