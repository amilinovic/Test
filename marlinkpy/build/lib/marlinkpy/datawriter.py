from marlinkpy import utility
import json
import csv
from pyspark.sql.functions import col
import pandas as pd

def write_csv(df,output_layer,root_folder,object_name,process_mode,year_str,month_str,day_str):
  # define output path for DataFrame
  write_file_path = f"/dbfs/mnt/{output_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/{object_name}_{process_mode}_{year_str}_{month_str}_{day_str}.csv"
  # define the output path for schema metadata
  write_meta_path = f"/dbfs/mnt/{output_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/metadata/{object_name}_{process_mode}_{year_str}_{month_str}_{day_str}.txt"
  
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

  # write file to cleanse layer
  (
    df
    .toPandas()
    .to_csv(
      write_file_path
      ,sep=";"
      ,header=True
      ,index=False
      ,quoting=csv.QUOTE_MINIMAL
      ,escapechar='"'
      ,doublequote=True
    )
  )
  # confirm writing of dataframe
  print(f"Succesfully written DataFrame to {output_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/")

def write_json(collection,output_layer,root_folder,object_name,process_mode,year_str,month_str,day_str):  
  # define file path
  write_file_path = f"/dbfs/mnt/{output_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/{object_name}_{process_mode}_{year_str}_{month_str}_{day_str}.json"
  # create directoy paths to prevent FileNotFound errors
  utility.create_directory(write_file_path)
  # write to datalake
  with open(write_file_path, "w") as outfile:
    json.dump(collection, outfile)
  # confirm writing of dataframe
  print(f"Succesfully written JSON to {output_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/")