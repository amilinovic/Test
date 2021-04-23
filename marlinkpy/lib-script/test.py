#!/usr/bin/python3

import subprocess
import wheel
import setuptools
import twine

cd /home/vsts/work/1/s/marlinkpy
python3 setup.py sdist bdist_wheel

var = subprocess.check_output('git diff --name-only --diff-filter=AMR HEAD^1 HEAD | xargs -I '{}' cp --parents -r '{}' $(Build.BinariesDirectory)')

echo $var

#newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)