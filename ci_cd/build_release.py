#!/usr/bin/python3

import os
import subprocess
import json

print('Just a test of script')

files = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

newfiles = files.decode("utf-8").split("/")[0]

print(newfiles)

if newfiles == "darabricks":
  print(newfiles + "Added file for databricks")
else:
  print("Added file for marlinkpy")

# Moze da se doda da ako je editovaj databricks folder da pokrene ovaj pipeline. A ako je editovan marlinkpy da pokrene drugi pipeline
# if newfiles.decode("utf-8") == '':
#   print('No added files. Exiting.')
#   exit(0)

