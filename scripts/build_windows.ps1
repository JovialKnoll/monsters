cd ..
# cleanup old build
rm -r dist
# use virtual environment
src/venv/Scripts/activate
# get pyinstaller
pip install pyinstaller
# create spec file
# --icon ICON_FILE
pyinstaller --clean -ywF --name chikkai src/main.py
# build exe
pyinstaller -y chikkai.spec
# copy in assets
cp -r src/assets dist/assets
# cleanup
deactivate
rm -r build
rm chikkai.spec
cd scripts
