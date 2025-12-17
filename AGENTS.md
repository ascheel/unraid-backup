# Purpose
This is a project that will ultimately create an unRAID docker container.  This project has the following attributes.
    - rsync will be used to copy data.
    - There will be 2 volumes inside of the container
        - /mnt/user         -> /source - read-only and available for reading data for backups
        - /mnt/user/backups -> /dest   - normal mount used to write backups
    - Backups will execute daily for 30 days.
    - Backups will be scheduled via a cron job.
