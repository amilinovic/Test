#!/usr/bin/python3

import os
import subprocess
import json

newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

newfileslist = newfiles.decode("utf-8").splitlines()

print(newfileslist)

for addedfile in newfileslist:
  name_directory = os.path.splitext(addedfile)[0].split("/")   #addedfile.decode("utf-8").split("/")[0]
  directory = name_directory[0]
  # print(directory)
  # run_databrick_commands = True

  if directory == 'databricks':
    print(directory + ' Added file for databricks ' + addedfile)
    print('##vso[task.setvariable variable=projectName;isOutput=true;]'project_name)
    
  else:
    print('No added files to databricks. Exiting.')

# Moze da se doda da ako je editovaj databricks folder da pokrene ovaj pipeline. A ako je editovan marlinkpy da pokrene drugi pipeline
# if newfiles.decode("utf-8") == '':
#   print('No added files. Exiting.')
#   exit(0)

