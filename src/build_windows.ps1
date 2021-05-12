rm -r build
rm -r dist
rm chikkai.spec
venv/Scripts/activate
pip install pyinstaller
# --icon ICON_FILE
pyinstaller --clean -ywF --name chikkai main.py
pyinstaller -y chikkai.spec
cp -r assets dist/assets
