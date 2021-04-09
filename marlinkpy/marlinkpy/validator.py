from marlinkpy import datareader
from pyspark.sql.functions import col
import os

#checks if acc and prd has the same amount of length in columns & rows   
def validate_metadata(sourceDF, targetDF):
  
  #checks for columns in targetDF(cleansed with u-sql) that are missing in sourceDF(cleansed with databricks)
  for column in targetDF.columns:
    if column not in sourceDF.columns:
      print(f"WARNING: Column missing from sourceDF -",column)
  #checks for columns in sourceDF(cleansed with databricks) that are missing in targetDF(cleansed with u-sql)
  for column in sourceDF.columns:
    if column not in targetDF.columns:
      print(f"WARNING: Column in sourceDF not in targetDF",column)
 
  try:
    #check the columns in sourceDF and targetDF
    assert len(targetDF.columns) == len(sourceDF.columns)
    print("All the columns are same")
  except:
      print("WARNING: the count of columns are different!")
      
  try:
    #check the amount of length in sourceDF and targetDF
    assert targetDF.count() == sourceDF.count()
    print("Count the DataFrames are equal")
  except:
    print("WARNING: Count of DataFrames are not equal!")

#casts the correct data types to targetDF 
def cast_datatypes(sourceDF,targetDF):
   #casts correct dtypes to targetDF
  for col_, type_ in sourceDF.dtypes:
        targetDF = targetDF.withColumn(col_, col(col_).cast(type_))
  return targetDF

#iterates through all the rows of individual columns in acc and prd
def validate_df(sourceDF,targetDF):
  abs_count = abs(targetDF.count() - sourceDF.count())
  list_ = []
  if abs_count == 0:
    for col_, type_ in sourceDF.dtypes:
      try:
        assert sourceDF.groupBy(col_).count().orderBy(col_).exceptAll(targetDF.groupBy(col_).count().orderBy(col_)).count() == 0
        print(f"Column {col_} passed the validation test")
      except:
        list_.append(col_)
        print(f"Column {col_} failed the validation test")
  else:
    print(f"Manual validation required for this dataset")
  return list_

def identify_mismatched_rows(id_,col_,sourceDF,targetDF):
  """
  Displays the records in sourceDF which are not present in targetDF. For example:
  id_(unique column) = 'Ref'
  col_ (Column to be validated) = "StartDate"  
  """
  tmpDF = (sourceDF.select(col(id_),col(col_)).exceptAll(targetDF.select(col(id_),col(col_))).distinct())
  return tmpDF