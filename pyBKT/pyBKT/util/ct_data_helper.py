from urllib.request import urlopen
from pyBKT.util import model_helper
import numpy as np

def ct_data(url, skill_name=None, resource_name=None, gs_name=None):
  s = urlopen(url)
  converted_data=[]
  counter = 0
  column_to_idx = {}
  for i in s:
      i = i.decode('utf-8')
      
      r = i.split()
      if(r[0] == "Row"):
          for j in r:
              column_to_idx[j] = counter
              counter += 1
          counter = 0
      elif len(r) > 22 and r[20].isdigit() and r[22].isdigit():
        for j in range(int(r[20])):
          converted_data.append({})
          converted_data[counter]["user_id"] = r[1]
          converted_data[counter]["correct"] = 1
          if resource_name is not None:
            converted_data[counter]["resource"] = r[column_to_idx[resource_name]]
          if gs_name is not None:
            converted_data[counter]["gs"] = r[column_to_idx[gs_name]]
          counter +=1 
        for j in range(int(r[22])):
          converted_data.append({})
          converted_data[counter]["user_id"] = r[1]
          converted_data[counter]["correct"] = 2
          if resource_name is not None:
            converted_data[counter]["resource"] = r[column_to_idx[resource_name]]
          if gs_name is not None:
            converted_data[counter]["gs"] = r[column_to_idx[gs_name]]
          counter +=1 
  return model_helper.convert_data(converted_data)