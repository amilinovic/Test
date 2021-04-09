from marlinkpy import utility
import json, os
from pyspark.sql.functions import col, lit
import pandas as pd

def write_csv(df,output_layer,file_path):
  # define the output path for schema metadata
  write_meta_path = f"/dbfs/mnt/{output_layer}/metadata/{file_path}.txt"
  write_file_csv =  f"/dbfs/mnt/{output_layer}/{file_path}.csv"
  write_file_path = f"/mnt/{output_layer}/{file_path}"
  # create directoy paths to prevent FileNotFound errors
  utility.create_directory(write_file_path)
  utility.create_directory(write_meta_path)
  # save schema to string variable
  ddl_string = ",".join([x+" "+y.upper() for (x,y) in df.dtypes])
  # Save string to metadata
  file = open(write_meta_path,"w") 
  file.write(ddl_string)
  file.close()

  # get list of columns with datatype timestamp
  special_columns = [x for (x,y) in df.dtypes if y in ["timestamp","int","long"]]
  for column in special_columns:
    df = df.withColumn(column, col(column).cast("string"))
  
  (
    df
    .coalesce(1)
    .write
    .csv(
      path=write_file_path
      ,mode="overwrite"
      ,encoding="UTF-8"
      ,header="true"
      ,quote='"'
      ,escape='"'
      ,sep=";"
      ,escapeQuotes=True
      ,nullValue=u"\u0000"
      ,emptyValue=u"\u0000"
    )
  )
  os.system(f"cat /dbfs{write_file_path}/part* > {write_file_csv}")
  
  print(f"Succesfully written DataFrame to {file_path}")

def write_delta(df,output_layer,file_path, mode="overwrite", partitionBy=[]):
  # format write file path
  write_file_path = f"/mnt/{output_layer}/{file_path}"
  if len(partitionBy) >= 1:
    # write parquet using native spark
    (   
      df
      .write
      .format("delta")
      .option("mergeSchema", "true")
      .mode(mode)
      .partitionBy(partitionBy)
      .save(write_file_path)
    )
    # confirm writing of dataframe
    print(f"Succesfully written DataFrame to {write_file_path}")
  else:
    # write parquet using native spark
    (   
      df
      .write
      .format("delta")
      .option("mergeSchema", "true")
      .mode(mode)
      .save(write_file_path)
    )
    # confirm writing of dataframe
    print(f"Succesfully written DataFrame to {write_file_path}")

def write_parquet(df,output_layer,file_path, mode="overwrite"):
  # format write file path
  write_file_path = f"/mnt/{output_layer}/{file_path}"
  # write parquet using native spark
  (   
    df
    .write
    .parquet(
      path=write_file_path
      ,mode=mode
      )
  )
  # confirm writing of dataframe
  print(f"Succesfully written DataFrame to {file_path}")

def write_json(collection,output_layer,file_path):  
  # define file path
  write_file_path = f"/dbfs/mnt/{output_layer}/{file_path}.json"
  # create directoy paths to prevent FileNotFound errors
  utility.create_directory(write_file_path)
  # write to datalake
  with open(write_file_path, "w") as outfile:
    json.dump(collection, outfile)
  # confirm writing of dataframe
  print(f"Succesfully written JSON to {file_path}")
