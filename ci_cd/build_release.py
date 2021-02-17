#!/usr/bin/python3

import os
import subprocess
import json

print('Just a test of script')

newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

print(newfiles)