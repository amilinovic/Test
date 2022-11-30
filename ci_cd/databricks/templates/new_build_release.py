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
addfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)
removedfiles = subprocess.check_output('git diff --diff-filter=D --name-only HEAD^ HEAD',shell=True)

# Added files to list
addfileslist = addfiles.decode("utf-8").splitlines()
removedfileslist = removedfiles.decode("utf-8").splitlines()

# Source path
src = '/home/vsts/work/1/s'

def add_files():
  for addedfile in addfileslist:
    name_directory = os.path.splitext(addedfile)[0].split("/")
    # Get name of his directory
    directory = name_directory[0]

    if directory == 'databricks':
      print(' Added file for databricks is: ' + addedfile)
      # Create workspace path for creating directory in Databricks
      workspace = name_directory[1:-1]
      workspace_path = "/".join(workspace)
      # Create target path for adding notebook to Databricks
      target = name_directory[1:]
      target_path = "/".join(target)
      # Tst must be env variable
      workspace_api = WorkspaceApi(api_client)
      workspace_directory = workspace_api.mkdirs(workspace_path = "/"+os.getenv('ENV')+"/"+workspace_path)
      workspace_import = workspace_api.import_workspace(
        source_path = src+"/"+addedfile,
        target_path = "/"+os.getenv('ENV')+"/"+target_path,
        is_overwrite = "true",
        fmt = "SOURCE",
        language = "PYTHON"
        )

print(add_files())







# print(newfiles)

# Added files to list
# newfileslist = newfiles.decode("utf-8").splitlines()
# # print(newfileslist)

# # # Source path
# src = '/home/vsts/work/1/s'
# # # Destination path
# # os.mkdir('/tmp/notebooks')
# # dest = '/tmp/notebooks'

# for addedfile in newfileslist:
#   name_directory = os.path.splitext(addedfile)[0].split("/")
#   # # Get name of his directory
#   directory = name_directory[0]
#   # # Get a name of project
#   # project_name = name_directory[1]
#   # print(name_directory)

#   if directory == 'databricks':
#     print(' Added file for databricks is: ' + addedfile)
#     # Create workspace path for creating directory in Databricks
#     workspace = name_directory[1:-1]
#     workspace_path = "/".join(workspace)
#     # Create target path for adding notebook to Databricks
#     target = name_directory[1:]
#     target_path = "/".join(target)
# # Tst must be env variable
#     workspace_api = WorkspaceApi(api_client)
#     workspace_directory = workspace_api.mkdirs(workspace_path = "/Tst/"+workspace_path)
#     workspace_import = workspace_api.import_workspace(
#       source_path = src+"/"+addedfile,
#       target_path = "/Tst/"+target_path,
#       is_overwrite = "true",
#       fmt = "SOURCE",
#       language = "PYTHON"
#       )






#     else:
#       workspace_api = WorkspaceApi(api_client)
#       workspace_directory = workspace_api.mkdirs(workspace_path = "/Tst/"+project_name)
#       workspace_import = workspace_api.import_workspace(
#         source_path = src+"/"+addedfile,
#         target_path = "/Tst/"+project_name+"/"+name_directory[2],
#         is_overwrite = "true",
#         fmt = "SOURCE",
#         language = "PYTHON"
#       )
