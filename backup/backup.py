import datetime
import os
import shlex
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

    def run_backup(self, name: str):
        try:
            job = self.config['jobs'][name]
        except KeyError:
            print(f"Job {name} not found in config")
            return

        excludes = self.get_excludes(name)

        destdir = os.path.join(job['destdir'], datetime.datetime.now().strftime("%Y-%m-%d-%H%M"))

        command = [
            "rsync",
            "-av",
            *excludes,
            job['srcdir'],
            destdir
        ]
        print(" ".join(command))

        # proc = subprocess.run(
        #     shlex.split(command),
        #     capture_output=True,
        #     text=True,
        #     check=False
        # )
        # if proc.returncode != 0:
        #     print(f"Error: {proc.stderr}")
        #     return
        
        print(f"Backup {name} completed successfully")


    def backup(self):
        for job in self.config['jobs']:
            self.run_backup(job)


def main():
    """
    Main entry point for the backup script.
    """
    with open('backup.yml', 'r') as f:
        config = yaml.safe_load(f)
    print(config)

if __name__ == "__main__":
    main()
