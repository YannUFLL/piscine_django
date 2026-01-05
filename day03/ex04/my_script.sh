set -e

rm -rf django_venv

python3 -m venv django_venv

./django_venv/bin/pip install -r requirement.txt

echo "Environment is ready. Switching to interactive mode..."

exec bash --rcfile <(echo "source ~/.bashrc; source django_venv/bin/activate"