FROM alpine:latest

RUN apk add --no-cache dcron python3 p7zip

RUN mkdir -p /backup
ADD backup /backup

COPY rsync.cron /etc/cron.d/rsync.cron

RUN chmod 0644 /etc/cron.d/rsync.cron /backup/backup.py /backup/backup.yml /backup/backup.sh

CMD ["crond", "-f"]
