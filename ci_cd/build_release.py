#!/usr/bin/python3

import os
import subprocess
import json

print('Just a test of script')

newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

newfileslist = newfiles.decode("utf-8").splitlines()

print(newfileslist)

for addedfile in newfileslist:
  name_pipeline = os.path.splitext(addedfile)[0].split("/")   #addedfile.decode("utf-8").split("/")[0]

  if name_pipeline == "databricks":
    print(name_pipeline + "Added file for databricks" + addedfile)
  else:
    print("Added file for marlinkpy")

# Moze da se doda da ako je editovaj databricks folder da pokrene ovaj pipeline. A ako je editovan marlinkpy da pokrene drugi pipeline
# if newfiles.decode("utf-8") == '':
#   print('No added files. Exiting.')
#   exit(0)

