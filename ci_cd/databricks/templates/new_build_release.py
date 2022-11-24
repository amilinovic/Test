#!/usr/bin/python3

import os
import subprocess
import shutil 
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.workspace.api import WorkspaceApi, WorkspaceFileInfo

api_client = ApiClient(
  host  = os.getenv('DATABRICKS_HOST'),
  token = os.getenv('DATABRICKS_TOKEN')
)

# Check git difference
newfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)

print(newfiles)

# Added files to list
newfileslist = newfiles.decode("utf-8").splitlines()
print(newfileslist)

# Source path
src = '/home/vsts/work/1/s'
# Destination path
os.mkdir('/tmp/notebooks')
dest = '/tmp/notebooks'

for addedfile in newfileslist:
  name_directory = os.path.splitext(addedfile)[0].split("/")
  # Get name of his directory
  directory = name_directory[0]
  # Get a name of project
  project_name = name_directory[1]
  print(name_directory)

  if directory == 'databricks':
    print(' Added file for databricks is: ' + addedfile)
    
    # shutil.copy(addedfile, dest)
    # files = os.listdir(dest)
    # print(files)
    if name_directory[3] == []:
      workspace_api = WorkspaceApi(api_client)
      workspace_import = workspace_api.import_workspace(
        source_path = src+"/"+addedfile,
        target_path = "/Tst/"+project_name+"/"+name_directory[2],
        is_overwrite = "true",
        fmt = "SOURCE",
        language = "PYTHON"
      )
    else:
      workspace_api = WorkspaceApi(api_client)
      workspace_import = workspace_api.import_workspace(
        source_path = src+"/"+addedfile,
        target_path = "/Tst/"+project_name+"/"+name_directory[2]+"/"+name_directory[3],
        is_overwrite = "true",
        fmt = "SOURCE",
        language = "PYTHON"
      )



os.mkdir('example_directory/')

    # files.append(addedfile[11:])
    # print(files)
    # if os.path.exists(dest):
    #   pass
    # else:
    #   shutil.copytree(src, dest)
