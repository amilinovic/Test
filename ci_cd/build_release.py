#!/usr/bin/python3

import os
import shutil
import subprocess
import json

# Check git difference
newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

original = "/home/vsts/work/1/s"
target = "/home/vsts/work/1/databricks"

if os.path.isdir(target) == True:
  os.remove(target)
  # shutil.copytree(original, target)
  print('Deleted directory')
else:
  print('Did not delete the directory')

newfileslist = newfiles.decode("utf-8").splitlines()

for addedfile in newfileslist:
  name_directory = os.path.splitext(addedfile)[0].split("/")
  directory = name_directory[0]
  project_name = name_directory[1]

  if directory == 'databricks':
    print(directory + ' Added file for databricks ' + addedfile)

    # Copy files to databricks directory
    shutil.copytree(original, target)

    # Pass variables from script to azure devops pipeline
    print('##vso[task.setvariable variable=directory;]%s' % (directory))
    print('##vso[task.setvariable variable=project_name;]%s' % (project_name))

  else:
    print('No added files to databricks. Exiting.')
