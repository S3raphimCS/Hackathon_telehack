FROM certbot/certbot:v1.27.0

LABEL MAINTAINER: Andrew Medvedev hydra1337channel@gmail.com

COPY certify-init.sh /opt/
RUN chmod +x /opt/certify-init.sh

ENTRYPOINT []
CMD ["certbot", "renew"]