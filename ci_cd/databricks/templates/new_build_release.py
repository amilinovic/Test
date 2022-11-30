#!/usr/bin/python3

import os
import subprocess
import shutil
from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.workspace.api import WorkspaceApi

api_client = ApiClient(
  host  = os.getenv('DATABRICKS_HOST'),
  token = os.getenv('DATABRICKS_TOKEN')
)

# Check git difference
addfiles = subprocess.check_output('git diff --diff-filter=AMR --name-only HEAD^ HEAD',shell=True)
removedfiles = subprocess.check_output('git diff --diff-filter=D --name-only HEAD^ HEAD',shell=True)

# Added files to list
addfileslist = addfiles.decode("utf-8").splitlines()
removefileslist = removedfiles.decode("utf-8").splitlines()

# Source path
src = '/home/vsts/work/1/s'

def add_files():
  for added_file in addfileslist:
    name_directory = os.path.splitext(added_file)[0].split("/")
    # Get name of his directory
    directory = name_directory[0]
    # If file is in databricks directory on repo
    if directory == 'databricks':
      print(' Added file for databricks is: ' + added_file)
      # Create workspace path for creating directory in Databricks
      workspace = name_directory[1:-1]
      workspace_path = "/".join(workspace)
      # Create target path for adding notebook to Databricks
      target = name_directory[1:]
      target_path = "/".join(target)
      workspace_api = WorkspaceApi(api_client)
      # Create directory in databricks if not exists
      workspace_directory = workspace_api.mkdirs(workspace_path = "/"+os.getenv('ENV')+"/"+workspace_path)
      # Import Notebook to Databricks
      workspace_import = workspace_api.import_workspace(
        source_path = src+"/"+added_file,
        target_path = "/"+os.getenv('ENV')+"/"+target_path,
        is_overwrite = "true",
        fmt = "SOURCE",
        language = "PYTHON"
        )
  return "There is no files to add!"

def remove_files():
  for removed_file in removefileslist:
    name_directory = os.path.splitext(removed_file)[0].split("/")
    # Get name of his directory
    directory = name_directory[0]
    # If file is in databricks directory on repo
    if directory == 'databricks':
      print(' Removed file from databricks is: ' + removed_file)
      # Create path of a notebook to delete it from Databricks
      notebook = name_directory[1:]
      delete_notebook = "/".join(notebook)
      workspace_api = WorkspaceApi(api_client)
      # Remove notebook from Databricks
      notebook_delete = workspace_api.delete(
        workspace_path = "/"+os.getenv('ENV')+"/"+delete_notebook,
        is_recursive = "false"
      )
  return "There is no files to remove!"

print(add_files())
print(remove_files())
