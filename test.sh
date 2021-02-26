#!/bin/bash

# databricks configure --token <<EOF
# https://adb-1542076191847040.0.azuredatabricks.net/
# dapi55d363f39ae62c3bfab47147858fe2ed-2
# EOF

# databricks clusters list --output JSON

# CLUSTER_OBJ=$(databricks clusters list --output JSON)
# CLUSTER_NAME=$(echo "dbs-cluster-"${{parameters.environment}} | tr [:upper:] [:lower:])
# CLUSTER_ID=$(echo $CLUSTER_OBJ | jq -r ".clusters[] | select(.cluster_name==\"$CLUSTER_NAME\") | .cluster_id")
# databricks clusters start --cluster-id $CLUSTER_ID
# sleep 5m



CLUSTER_OBJ=$(databricks clusters list --output JSON)
CLUSTER_NAME=$(echo "test-cluster" | tr [:upper:] [:lower:])
CLUSTER_ID=$(echo $CLUSTER_OBJ | jq -r ".clusters[] | select(.cluster_name==\"$CLUSTER_NAME\") | .cluster_id")
databricks clusters start --cluster-id $CLUSTER_ID
while true;
do
  CLUSTER_STATE=$(databricks clusters list --output JSON | jq -r ".clusters[] | select(.cluster_name==\"$CLUSTER_NAME\") | .state")
  if [ $CLUSTER_STATE == "RUNNING" ]
    then
      break
    else
      sleep 10s
    fi
done
echo "Cluster is running!!"
# CLUSTER_STATE=$(databricks clusters list --output JSON | jq -r ".clusters[] | select(.cluster_name==\"$CLUSTER_NAME\") | .state")
# echo $CLUSTER_STATE