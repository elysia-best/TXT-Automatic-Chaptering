# !/bin/bash
pyi-makespec -F -w --osx-bundle-identifier "ga.swjtu.txt-sort" --codesign-identity "Developer ID Application: Yinan Qin (LGGLY4BBY7)" -n "TXT-Automatic-Chaptering" -i src/logo/logo_rounded.ico main.py
pyinstaller --clean -y TXT-Automatic-Chaptering.spec
# https://github.com/create-dmg/create-dmg