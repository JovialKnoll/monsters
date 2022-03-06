cd ../../jovialengine
python -m build --sdist --wheel --outdir dist/ . | Out-Null
cd ../monsters
src/venv/Scripts/activate.ps1
pip install --force-reinstall ../jovialengine/dist/jovialengine-VERSION-py3-none-any.whl  | Out-Null
python src/main.py
deactivate
cd scripts
