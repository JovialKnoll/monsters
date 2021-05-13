rm -r dist
src/venv/Scripts/activate
pip install pyinstaller
# --icon ICON_FILE
pyinstaller --clean -ywF --name chikkai src/main.py
pyinstaller -y chikkai.spec
cp -r src/assets dist/assets
rm -r build
rm chikkai.spec
