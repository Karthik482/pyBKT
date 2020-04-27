from urllib.request import urlopen
from pyBKT.util import model_helper
import numpy as np

def ct_data(url, skill_name, resource_col=None, gs_col=None, multilearns2=False, multipriors=False):
  s = []
  if url[:4] == "http":
    s = urlopen(url)
  else:
    f = open("data/" + url, "r")
    temp = f.readline()
    while temp is not "":
      s.append(temp)
      temp = f.readline()
  converted_data=[]
  counter = 0
  column_to_idx = {}
  for i in s:
      if not isinstance(i, str):
          i = i.decode('utf-8')
      r = i.split()
      if len(r) > 19 and r[19].isdigit() and r[5] == skill_name:
          correct = int(r[19])
          if correct == 0 or correct == 1:
              converted_data.append({})
              converted_data[counter]["user_id"] = r[1]
              converted_data[counter]["correct"] = correct
              if resource_col is not None:
                converted_data[counter]["resource"] = r[resource_col]
              if gs_col is not None:
                converted_data[counter]["gs"] = r[gs_col]
              counter +=1 
  return model_helper.convert_data(converted_data, multipriors)