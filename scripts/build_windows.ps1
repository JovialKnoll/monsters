cd ..
# cleanup old build
rm -r dist
# use virtual environment
src/venv/Scripts/activate.ps1
# get pyinstaller
pip install pyinstaller
# create spec file
pyinstaller --clean -ywF -i design/icon.ico -n chikkai src/main.py
# build exe
pyinstaller -y chikkai.spec
# copy in assets
cp -r src/assets dist/chikkai/assets
mv dist/chikkai.exe dist/chikkai/
# cleanup
deactivate
rm -r build
rm chikkai.spec
cd scripts
