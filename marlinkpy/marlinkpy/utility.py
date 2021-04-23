import os
import re

def extract_file_date(path_str):
  path_list = path_str.split("/")
  new_path_list = []
  for element in path_list:
    try:
      int(element)
      new_path_list.append(element)
    except:
      pass
  file_date = "".join(new_path_list)
  return file_date

def generate_delta_path(path_str):
  # split path on "/"
  path_list = path_str.split("/")
  # extract last element of path_list and 0th element after splitting on "_"
  object_name = path_list[-1].split('_')[0]
  # Initialise list
  new_path_list = []
  # If element is not integer add to list, else break loop
  for i in range(len(path_list)):
    try:
      int(path_list[i])
      break
    except:
      if (path_list[i] != object_name) and (i != len(path_list)-1):
        new_path_list.append(path_list[i])
      else:
        pass
  # generate new string
  new_path_str = "/".join(new_path_list) + f"/delta/{object_name}"
  
  return new_path_str

def create_directory(path_str):
  # create list by splitting string based on slash icon
  path_list = path_str.split('/')[:-1]
  # iterate through list and create directories starting from position 2
  for i, x in enumerate(path_list):
    tmp_obj = "/".join(path_list[:i+1])
    tmp_path = f"{tmp_obj}"
    try:
      os.mkdir(tmp_path)
      print(f"{tmp_path} created.")
    except:
      pass

def usql_to_pyspark_script(query_string, column_names):
    # prepare column_names
    special_columns_original = [x for x in column_names if ("_" in x)]
    special_columns_transformed = [x.replace("_","") for x in special_columns_original]
    # populate dictionary with transformed(key) and original(value) pairs
    column_dictionary = {}
    for i in range(len(special_columns_original)):
      column_dictionary.update({special_columns_transformed[i]:special_columns_original[i]})

    # convert USQL SELECT to pyspark .select
    query_string = re.sub(r"(?is)SELECT ",".select(",query_string)
    # convert USQL AS to pyspark .alias
    query_string = re.sub(r"(?is) AS ",".alias(\"",query_string)
    # close evert line with closing parentheses
    query_string = re.sub(r"(?is),\n","\"),\n",query_string)
    # remove underscore '_' to facilitate REGEX
    query_string = query_string.replace("_","")
    # replace USQL [COLUMN_NAME] with pyspark "COLUMN_NAME"
    query_string = query_string.replace("[","\"")
    query_string = query_string.replace("]","\"")
    # remove spaces
    query_string = query_string.replace(" ","")
    # generate foundation for query string
    query_list_before = query_string.split("\n")
    query_list_after = [q for q in query_list_before if (q != "")]
    query_string = "\n".join(query_list_after)+")"
    # process Integers
    query_string = re.sub(r"func.Number.ParseNullInt\(\"(?=[A-Za-z]{1,20})","col(\"",query_string)
    query_list_before_int = query_string.split("\n")
    query_list_after_int = [q.split(".")[0]+".cast(\"int\")."+q.split(".")[1] if ((q[:4] != "func") and (len(q.split(".")) == 2) and (q[0] != ".")) else q for q in query_list_before_int]
    query_string = "\n".join(query_list_after_int)
    # process DateTime
    query_string = re.sub(r"func.Date.ParseNullDateTime\(\"(?=[A-Za-z]{1,20}\",)","to_timestamp(col(\"",query_string)
    query_list_before_datetime = query_string.split("\n")
    query_list_after_datetime = [q.split(",")[0]+"),format=timestamp_format)."+q.split(".")[-1] if (q[:4] == "date") else q for q in query_list_before_datetime]
    query_string = "\n".join(query_list_after_datetime)
    # process Date
    query_string = re.sub(r"func.Date.ParseNullDateTime\(\"(?=[A-Za-z]{1,20})","col(\"",query_string)
    query_list_before_date = query_string.split("\n")
    query_list_after_date = [q.split(".")[0]+".cast(\"date\")."+q.split(".")[1] if (len(q.split(".")) == 2) and (q[:4]!="date") and (len(q.split(".")[0]) > 0) else q for q in query_list_before_date]
    query_string = "\n".join(query_list_after_date)
    # process String
    query_string = re.sub(r"func.String.RemoveDefaultRowDelimiters\(\"(?=[A-Za-z]{1,20})","datatypes.replace_default_row_delimiters_udf(col(\"",query_string)
    query_list_before_string = query_string.split("\n")
    query_list_after_string = [q.split(".alias")[0]+").alias"+q.split(".alias")[1] if q[:4]=="data" else q for q in query_list_before_string]
    query_string = "\n".join(query_list_after_string)
    # process Boolean
    query_string = re.sub(r"func.Boolean.ParseNullBoolean\(\"(?=[A-Za-z]{1,20}\".Trim())","trim(col(\"",query_string)
    query_list_before_boolean = query_string.split("\n")
    query_list_after_boolean = [q.split(".Trim()")[0]+")).cast(\"boolean\").alias"+q.split(".alias")[-1] if (q[:4]=="trim") else q for q in query_list_before_boolean]
    query_string = "\n".join(query_list_after_boolean)
    # prettify output
    query_string = query_string.replace("\"\"","\"")
    # replace special column names
    for key in column_dictionary:
      query_string = query_string.replace(key,column_dictionary[key],1)
    # prettify output
    query_string = query_string.replace("\"\"","\"")
    
    # format pyspark query
    query_list_before_format = query_string.split("\n")
    query_list_after_format = [x for x in query_list_before_format]
    start_of_string = "cleansedDF = (\n  rawDF\n  "
    end_of_string = "\n  )\n)"
    query_string = start_of_string + "\n    ".join(query_list_after_format) + end_of_string
    
    # print output to notebook
    print(query_string)

def hello():
    print("Hello World")

def hello2():
    print("Hello World #1")