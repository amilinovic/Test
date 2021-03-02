def read_json(spark,input_layer,root_folder,object_name,process_mode,year_str,month_str,day_str):
  # define file path
  read_file_path = f"/mnt/{input_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/{object_name}_{process_mode}_{year_str}_{month_str}_{day_str}.json"
  # read json as spark DataFrame
  df = spark.read.json(read_file_path, multiLine =True, primitivesAsString=True)
  return df

def read_csv(spark,input_layer,root_folder,object_name,process_mode,year_str,month_str,day_str,header="true",encoding="UTF-8",lineSep="\u0085",sep="\u0001",quote="",escape="",include_schema=False):
  # define input path for DataFrame
  read_file_path = f"/mnt/{input_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/{object_name}_{process_mode}_{year_str}_{month_str}_{day_str}.csv"
  if include_schema == True:
    # define the input path for schema metadata
    read_meta_path = f"/dbfs/mnt/{input_layer}/{root_folder}/{year_str}/{month_str}/{day_str}/metadata/{object_name}_{process_mode}_{year_str}_{month_str}_{day_str}.txt"
    # read json file with schema definition
    file = open(read_meta_path,"r") 
    schema = file.read()
    file.close()
    # read df from input layer
    df = spark.read.csv(read_file_path,schema=schema,header=header,encoding=encoding,sep=sep,lineSep=lineSep,quote=quote,escape=escape)
  else:
    df = spark.read.csv(read_file_path,inferSchema="false",header=header,encoding=encoding,sep=sep,lineSep=lineSep,quote=quote,escape=escape)
  return df
