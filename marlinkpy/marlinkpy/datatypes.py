from pyspark.sql.functions import lit, col, trim, to_timestamp, when, regexp_replace, to_date, pandas_udf, expr, concat, hex, unhex
import pandas as pd

def parse_int(column,thousands_separator=""):
  return trim(regexp_replace(column,thousands_separator,"")).cast("int")

def parse_bigint(column,thousands_separator=""):
  return trim(regexp_replace(column,thousands_separator,"")).cast("long")

def parse_boolean(column, true_value="true", false_value="false"):
  return when(column == true_value, lit(True)).when(column == false_value, lit(False)).otherwise(lit(None)).cast("boolean")

def parse_decimal(column, scale="30", precision="12", thousands_separator=",", decimal_separator="\."):
  return regexp_replace(regexp_replace(column,thousands_separator,""),decimal_separator,".").cast(f"decimal({scale},{precision})")

def parse_datetime(column, format="yyyy-MM-dd HH:mm:ss[.SSSSSSS]"):
  return to_timestamp(trim(column), format=format)

def parse_date(column, format="yyyy-MM-dd"):
  return to_date(trim(column), format=format)

@pandas_udf("string")
def cleanse_string(input_string: pd.Series) -> pd.Series:
  return input_string.str.replace("\r\n", "").str.replace("\r", "").str.replace("\n", "").str.strip()

def replace_default_row_delimiters(column):
  return when(cleanse_string(column) == '', lit(None)).otherwise(cleanse_string(column))

def replace_value(column, old_value, new_value=""):
  return regexp_replace(column,old_value,new_value)

def hex_to_byte(column, prefix_0x = True):
  if prefix_0x == True:
    return expr(f"unhex(substring({column},3,length({column})-2))")
  else:
    return expr(f"unhex({column})")

def byte_to_hex(column, prefix_0x = True):
  if prefix_0x == True:
    return concat(lit("0x"),hex(column))
  else:
    return hex(column)