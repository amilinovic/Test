# use pandas to read excel
import pandas as pd

def read_json(spark,input_layer,file_path):
  # define file path
  read_file_path = f"/mnt/{input_layer}/{file_path}.json"
  # read json as spark DataFrame
  df = spark.read.json(read_file_path, multiLine =True, primitivesAsString=True)
  return df

def read_delta(spark,input_layer,delta_path):
  # define input path for DataFrame
  read_delta_path = f"/mnt/{input_layer}/{delta_path}"
  df = spark.read.format("delta").load(read_delta_path)
  return df

def read_parquet(spark,input_layer,file_path):
  # define input path for DataFrame
  read_file_path = f"/mnt/{input_layer}/{file_path}"
  df = spark.read.parquet(read_file_path)
  return df

def read_excel(spark,input_layer,path_str,sheet_name=0,header=0,usecols=None):
  # define file path
  read_file_path = f"/dbfs/mnt/{input_layer}/{path_str}.xlsx"
  # read json as spark DataFrame
  df = spark.createDataFrame(pd.read_excel(read_file_path,sheet_name=sheet_name,dtype=str,header=header,usecols=usecols))
  return df

def read_csv(spark,input_layer,file_path,header="true",encoding="UTF-8",lineSep=None,sep=";",quote="",escape="", suffix=".csv"):
  """
  Parameters with None values will use pyspark default values. 
  
  Documentation: https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrameReader.csv.html
  """
  # define input path for DataFrame
  read_file_path = f"/mnt/{input_layer}/{file_path}{suffix}"
  # read csv
  df = spark.read.csv(read_file_path,inferSchema="false",header=header,encoding=encoding,sep=sep,lineSep=lineSep,quote=quote,escape=escape)
  return df
