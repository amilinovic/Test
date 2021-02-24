#!/usr/bin/python3

import os
import subprocess
import shutil 

# Check git difference
newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

# Added files to list
newfileslist = newfiles.decode("utf-8").splitlines()

# Source path
src = '/home/vsts/work/1/s'
# Destination path
dest = '/home/vsts/work/1/d/'

for addedfile in newfileslist:
  name_directory = os.path.splitext(addedfile)[0].split("/")
  # Get name of his directory
  directory = name_directory[0]
  # Get a name of project
  project_name = name_directory[1]
  

  if directory == 'databricks':
    print(' Added file for databricks is: ' + addedfile)

    if os.path.exists(dest):
      pass
    else:
      shutil.copytree(src, dest)

    # Pass variables from script to azure devops pipeline
    print('##vso[task.setvariable variable=directory;]%s' % (directory))
    print('##vso[task.setvariable variable=project_name;]%s' % (project_name))

  else:
    print('No added files to databricks dir.')
