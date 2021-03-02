# Getting started with marlinkpy
The marlinkpy python library provides us with a framework for developing our code in a standardized way. The functionality for building these templates are found in this repository. The following document will guide you in updating the marlinkpy library with new functionality.

## Structure
In this document we describe the following:
- Dependencies
- Adding/Updating python functions
- Committing to Azure DevOps
- Updating Azure Databricks with new marlinkpy library
- More information

## Dependencies
In order to follow allong with this manual you will need the following:
- Command prompt
- IDE (i.e. Visual Studio)
- Python3 interpreter

## Adding/Updating python functions
**Step 1: Create a feature branch for updating the marlinkpy python library**
Before we integrate new marlinkpy functionality we need to create a feature branch in [Azure DevOps](https://dev.azure.com/marlink/Marlink%20Digitalization/_git/mart-dbs/branches). Make sure to create your feature branch based on the `develop` branch.

**Step 2: Update code in repository**
Make sure that you have cloned the [Azure DevOps](https://dev.azure.com/marlink/Marlink%20Digitalization/_git/mart-dbs) repository locally and opened a feature branch in Visual Studio. Next, make changes to the marlinkpy folder by updating current udf or adding/removing udf's. Once you've completed saving your python changes it's time to compile the python library.

**Step 3: Command prompt operations**
In order for us to compile the marlinkpy python library we have to perform the following operations in sequence:
1. Open your command prompt.
2. Navigate to the marlinkpy folder in the repository. To navigate we use the `cd folderName` command. Tip: Use the `ls` (for linux) or `dir` (for windows) command to list elements in your current working directory. 
3. Activate the virtual environment: 
Linux users -> `source venv/bin/activate`, 
Windows users -> `.\venv\Scripts\activate`.
4. Install library dependencies using: `pip install -r /venv/requirements.txt`
5. Once in the repository and the virtual environment has been activated, use the following command to build the python library: `python setup.py bdist_wheel`

At the end of these steps you can confirm a new `.whl` file has been created in the `dist` folder. The wheel file needs to be synced with git and has to be installed on the databricks cluster.

## Committing to Azure DevOps
Assuming you've been working in a feature branch, continue with the following steps:
1. Go to git changes
2. Enter a commit messages
3. Commit All
4. Push the branch to Azure DevOps
5. Go to [Azure DevOps](https://dev.azure.com/marlink/Marlink%20Digitalization/_git/mart-dbs/branches) and create a Pull Request.
6. Perform a Pull Request from the feature branch to the develop branch.

## Updating Azure Databricks with new marlinkpy library
Once you've compiled the `.whl` file (or wheel) we can continue with updating the python library in Databricks. To install the newest version of the marlinkpy file, perform the following steps:
1. Navigate to the [Azure Databricks cluster](https://adb-4056835074975613.13.azuredatabricks.net/?o=4056835074975613#setting/clusters/0111-103209-flaw696/libraries).
2. Select Libraries
3. Select New
4. Select Library Source -> Upload, Library Type -> Python Whl
5. Drag the `.whl` file to the box, and click install.

## More information
The following [article](https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f) describes the steps, and even more possibilities, for building custom python libraries.