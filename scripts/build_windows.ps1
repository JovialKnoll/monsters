cd ..
# cleanup old build
rm -r dist
# use virtual environment
src/venv/Scripts/activate.ps1
# get pyinstaller
pip install pyinstaller
# create spec file
# --icon ICON_FILE
# --onefile
pyinstaller --clean -yw --name chikkai src/main.py
# build exe
pyinstaller -y chikkai.spec
# copy in assets
cp -r src/assets dist/chikkai/assets
# cleanup
deactivate
rm -r build
rm chikkai.spec
cd scripts
