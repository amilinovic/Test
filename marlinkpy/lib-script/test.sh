#!/usr/bin/bash

# import subprocess
# import wheel
# import setuptools
# import twine

cd /home/vsts/work/1/s/marlinkpy
# source venv/Scripts/activate
pip3 install wheel
pip3 install setuptools
pip3 install twine
python3 setup.py sdist bdist_wheel

var = subprocess.check_output('git diff --name-only --diff-filter=AMR HEAD^1 HEAD | xargs -I '{}' cp --parents -r '{}' $(Build.BinariesDirectory)')

echo $var

#newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)