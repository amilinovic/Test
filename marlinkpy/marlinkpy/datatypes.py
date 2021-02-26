import pandas as pd
from pyspark.sql.functions import pandas_udf, udf
from datetime import datetime
from pytz import timezone

@udf('string')
def parse_null_datetime_udf(datetime_str, current_str_format):
  if (len(str(datetime_str)) > 4) and (int(datetime_str[:4]) > 1000):
    # define output string format
    cleansed_string_format = "%Y-%m-%dT%H:%M:%S.%f0%z"
    # define timezone
    tz = timezone("Canada/Pacific")
    # convert string input to datetime object
    datetime_object = datetime.strptime(datetime_str, current_str_format)
    # apply timezone
    localized_datetime_object = tz.localize(datetime_object)
    # formatted string with datetime
    string_formatted_datetime = localized_datetime_object.strftime(cleansed_string_format)
    # format return value
    return_value = string_formatted_datetime[:-2] + ":00" 
  else:
    return_value = None
  return return_value

@pandas_udf("string")
def format_datetime_string_udf(input_string: pd.Series) -> pd.Series:
  if len(str(input_string)) >= 18:
    output_string = input_string.str[0:19]+".000Z"
  else:
    output_string = None
  return output_string

# vectorized udf
@pandas_udf("string")
def replace_default_row_delimiters_udf(input_string: pd.Series) -> pd.Series:
  if len(str(input_string)) > 0:
    output_string = input_string.str.replace("\r\n", "").str.replace("\r", "").str.replace("\n", "").str.strip()
  else:
    output_string = None
  return output_string