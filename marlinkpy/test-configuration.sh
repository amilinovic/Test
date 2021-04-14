#!/bin/bash

pip3 install databricks-cli

databricks configure --token <<EOF
https://adb-4885809453486256.16.azuredatabricks.net/
dapi254bc815c52e8574d24b1402a381cca0-2
EOF

databricks fs cp $(Pipeline.Workspace)/python_library/dist/marlinkpy-0.1.1-py3-none-any.whl dbfs:/FileStore/jars/marlinkpy-0.1.1-py3-none-any.whl --overwrite

# CLUSTER_OBJ=$(databricks clusters list --output JSON)
# CLUSTER_NAME=$(echo "test-cluster" | tr [:upper:] [:lower:])
# CLUSTER_ID=$(echo $CLUSTER_OBJ | jq -r ".clusters[] | select(.cluster_name==\"$CLUSTER_NAME\") | .cluster_id")
# {
# databricks libraries install --cluster-id $CLUSTER_ID --whl dbfs:/FileStore/jars/marlinkpy-0.1.1-py3-none-any.whl
# } || { 
# databricks clusters start --cluster-id $CLUSTER_ID
# sleep 5m
# databricks libraries install --cluster-id $CLUSTER_ID --whl dbfs:/FileStore/jars/marlinkpy-0.1.1-py3-none-any.whl
# }

# CLUSTER_OBJ=$(databricks clusters list --output JSON)
# CLUSTER_NAME=$(echo "test-cluster" | tr [:upper:] [:lower:])
# CLUSTER_ID=$(echo $CLUSTER_OBJ | jq -r ".clusters[] | select(.cluster_name==\"$CLUSTER_NAME\") | .cluster_id")
# databricks libraries install --cluster-id $CLUSTER_ID --pypi-package "xlrd==1.1.0"