#!/usr/bin/python3

import os
import subprocess
import json

newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

newfileslist = newfiles.decode("utf-8").splitlines()

for addedfile in newfileslist:
  name_directory = os.path.splitext(addedfile)[0].split("/")   #addedfile.decode("utf-8").split("/")[0]
  directory = name_directory[0]
  project_name = name_directory[1]
  # print(directory)
  # run_databrick_commands = True

  if directory == 'databricks':
    print(directory + ' Added file for databricks ' + addedfile)
    # print('$(project_name)')
    # print('##vso[task.setvariable variable=project_name;]%s' % (project_name))
    print "Current working dir : %s" % os.getcwd()
    
  else:
    print('No added files to databricks. Exiting.')
