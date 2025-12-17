import datetime
import os
import shutil
import subprocess
import yaml


class Backup:
    def __init__(self):
        self.config_file = "backup.yml"
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def get_excludes(self, name: str):
        output = []
        excludes = self.config['jobs'][name]['exclude']
        for exclude in excludes:
            output.append(f'--exclude="{exclude}"')
        return output

    def cleanup_old_backups(self, name: str):
        """Delete backups older than the retention period."""
        try:
            job = self.config['jobs'][name]
        except KeyError:
            print(f"Job {name} not found in config")
            return

        retention_days = job.get('retention', 30)
        destdir = job['destdir']
        
        if not os.path.exists(destdir):
            return

        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
        deleted_count = 0

        # List all directories in the backup destination
        for item in os.listdir(destdir):
            item_path = os.path.join(destdir, item)
            
            # Only process directories
            if not os.path.isdir(item_path):
                continue

            # Try to parse the directory name as YYYY-MM-DD-HHMM
            try:
                # Extract date part (first 10 characters: YYYY-MM-DD)
                date_str = item[:10]
                backup_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                
                # If backup is older than retention period, delete it
                if backup_date < cutoff_date:
                    print(f"Deleting old backup: {item} (from {backup_date.strftime('%Y-%m-%d')})")
                    shutil.rmtree(item_path)
                    deleted_count += 1
            except (ValueError, IndexError):
                # Skip directories that don't match the expected format
                print(f"Warning: Skipping directory with unexpected format: {item}")
                continue

        if deleted_count > 0:
            print(f"Cleaned up {deleted_count} old backup(s) for job {name}")
        else:
            print(f"No old backups to clean up for job {name}")

    def run_backup(self, name: str):
        try:
            job = self.config['jobs'][name]
        except KeyError:
            print(f"Job {name} not found in config")
            return

        excludes = self.get_excludes(name)

        srcdir = f"{job['srcdir']}/"
        destdir = os.path.join(job['destdir'], datetime.datetime.now().strftime("%Y-%m-%d-%H%M"))
        os.makedirs(destdir, exist_ok=True)

        command = [
            "rsync",
            "-av",
            *excludes,
            srcdir,
            destdir
        ]

        print(f"Executing command: {' '.join(command)}")

        proc = subprocess.run(
            command,
            text=True,
            check=False
        )
        if proc.returncode != 0:
            print(f"Error: Backup failed with return code {proc.returncode}")
            return
        
        print(f"Backup {name} completed successfully")
        
        # Clean up old backups after successful backup
        self.cleanup_old_backups(name)


    def backup(self):
        for job in self.config['jobs']:
            self.run_backup(job)


def main():
    """
    Main entry point for the backup script.
    """
    backup = Backup()
    backup.backup()

if __name__ == "__main__":
    main()
