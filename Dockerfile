FROM alpine:latest

RUN apk add --no-cache python3 p7zip curl rsync && \
    curl -L https://github.com/aptible/supercronic/releases/download/v0.2.26/supercronic-linux-amd64 \
    -o /usr/local/bin/supercronic && \
    chmod +x /usr/local/bin/supercronic

CMD ["supercronic", "/etc/cron.d/backup.cron"]

