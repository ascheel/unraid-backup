import yaml
import subprocess

def main():
    with open('backup.yml', 'r') as f:
        config = yaml.safe_load(f)
    print(config)

if __name__ == "__main__":
    main()
