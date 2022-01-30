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
# windows setup
mkdir dist/chikkai
mv dist/chikkai.exe dist/chikkai/chikkai.exe
# copy in assets
cp -r src/assets dist/chikkai/assets
# copy in readme
cp design/README.txt dist/chikkai/
# copy in license
cp LICENSE.txt dist/chikkai/
# cleanup
deactivate
rm -r build
rm chikkai.spec
cd scripts
