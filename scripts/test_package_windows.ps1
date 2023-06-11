cd ../../jovialengine
((Get-Content -path setup.cfg -Raw) -replace 'VERSION_REPLACE','999') | Set-Content -Path setup.cfg -NoNewline
python -m build --sdist --wheel --outdir dist/ . | Out-Null
((Get-Content -path setup.cfg -Raw) -replace '999','VERSION_REPLACE') | Set-Content -Path setup.cfg -NoNewline
cd ../monsters
src/venv/Scripts/activate.ps1
pip install --force-reinstall ../jovialengine/dist/jovialengine-999-py3-none-any.whl | Out-Null
python src/main.py
deactivate
cd scripts
