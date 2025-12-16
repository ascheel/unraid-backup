pushd /backup
echo "Starting backup..."
python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt

python3 backup.py --config backup.yml

popd
